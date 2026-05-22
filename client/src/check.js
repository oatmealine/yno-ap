// see build.mjs for importing logic
import locationsRaw from '@locations';

import { checkLocations, client as apClient, Goal, isLocationChecked, slotData } from './archipelago-client';
import { isSessionValid } from './dream-session';
import { getPos, getSwitch, getVariable, trackSwitch, waitForEvent, waitForPicture, waitForSwitchChange, waitForVariableChange } from './easyrpg-client';
import { saveSlot, slotStore } from './store';
import { showToastMessage } from './ui';

/** @type {Location[]} */
const locations = locationsRaw
  .map(location => {
    const conditions = location.conditions ?? singleton(location.condition);
    for (const condition of conditions) {
      condition.parent = location;
    }
    return location;
  })

// this is structured rather differently than yno-server's badges.go impl - this
// is mostly just because i like it better this way

/** 
  see README.md for actual docs
  @typedef {'' | 'event' | 'eventAction' | 'picture' | 'coords' | 'teleport' | 'prevMap'} TriggerType

  @typedef {Object} Location

  @property {string} name
  @property {Condition} [condition]
  @property {Condition[]} [conditions]
  @property {number} [conditionsCount]
  
  // non-serialized properties, inherited from the file structure
  @property {string} filename

  @typedef {Object} Condition
  @property {number} [map]

  @property {number} [switchId]
  @property {boolean} [switchValue]
  @property {number[]} [switchIds]
  @property {boolean[]} [switchValues]
  @property {boolean} [switchDelay]

  @property {number} [varId]
  @property {number} [varValue]
  @property {number} [varValue2]
  @property {'=' | '<' | '>' | '<=' | '>=' | '!=' | '>=<'} [varOp]
  @property {number[]} [varIds]
  @property {number[]} [varValues]
  @property {('=' | '<' | '>' | '<=' | '>=' | '!=')[]} [varOps]
  @property {boolean} [varDelay]
  @property {boolean} [varTrigger]

  @property {TriggerType} [trigger]
  @property {string} [value]
  @property {string[]} [values]
  @property {number} [mapX1]
  @property {number} [mapX2]
  @property {number} [mapY1]
  @property {number} [mapY2]

  @property {boolean} [timeTrial]

  // non-serialized properties, inherited from the file structure
  @property {string} identifier
  @property {Location} parent
 */

/**
 * locations to not stop listening for, as they are useful for things other than
 * sending locations
 * @param {Location} location
 */
function shouldAlwaysListenLocation(location) {
  // neccessary for goal checking
  if (slotData.endings.includes(location.name))
    return true;

  return false;
}

/**
 * @param {Condition} condition
 */
function isConditionComplete(condition) {
  return slotStore.completedConditions.includes(condition.identifier);
}

/**
 * @param {Location} location
 */
function isLocationComplete(location) {
  const conditions = location.conditions ?? singleton(location.condition);
  const neededConditionsCount = location.conditionsCount ?? conditions.length;
  const completedCount = conditions
    .filter(isConditionComplete)
    .length;

  return completedCount >= neededConditionsCount;
}

/**
 * for special location completion behavior, eg. goaling
 * @param {Location} location
 */
function onLocationComplete(location) {
  if (slotData.endings.includes(location.name)) {
    if (!slotStore.completedEndings.includes(location.name)) {
      slotStore.completedEndings.push(location.name);
    }

    let canGoal = false;
    if (slotData.goal === Goal.AllEndings) {
      const endingsDone = slotData.endings
        .filter(ending => slotStore.completedEndings.includes(ending))
        .length;
      const endingsNeeded = slotData.endings.length;
      canGoal = endingsDone >= endingsNeeded;
      showToastMessage(`<b>Goal</b>: ${endingsDone}/${endingsNeeded} endings done`);
    }
    if (slotData.goal === Goal.AnyEnding) {
      canGoal = true;
    }

    if (canGoal) {
      apClient.goal();
    }
  }
}

/**
 * @param {Location} location
 * @param {boolean} routine
 */
function updateLocationCompletion(location, routine = false) {
  if (isLocationComplete(location)) {
    console.log('[yno-ap-client] all conditions met: ', location.filename);
    
    checkLocations(location.name);
    if (!routine) onLocationComplete(location);

    // just for the sake of optimizing away checking them unneccessarily
    const conditions = location.conditions ?? singleton(location.condition);
    for (let condition of conditions)
      if (!isConditionComplete(condition))
        slotStore.completedConditions.push(condition.identifier);
    saveSlot();
  }
}

export function updateLocationCompletions() {
  for (const location of locations)
    updateLocationCompletion(location, true);
}

/**
 * @param {Condition} condition
 */
function markConditionAsComplete(condition) {
  console.log('[yno-ap-client] condition complete: ', condition);

  if (!isSessionValid()) return;

  if (!isConditionComplete(condition)) {
    slotStore.completedConditions.push(condition.identifier);
    saveSlot();
  }

  updateLocationCompletion(condition.parent);
}

/**
 * @param {Condition} condition 
 * @returns {boolean}
 */
function checkConditionCoords(condition) {
  const [x, y] = getPos();

  if (condition.mapX1 || condition.mapX2) {
    if (condition.mapX1 !== -1 && x < condition.mapX1)
      return false;
    if (condition.mapX2 !== -1 && x > condition.mapX2)
      return false;
  }
  if (condition.mapY1 || condition.mapY2) {
    if (condition.mapY1 !== -1 && y < condition.mapY1)
      return false;
    if (condition.mapY2 !== -1 && y > condition.mapY2)
      return false;
  }

  return true;
}

/**
 * @template A
 * @param {A} item
 * @returns {A[]}
 */
function singleton(item) {
  if (item !== undefined && item !== null)
    return [item];
  return [];
}

/**
 * @param {Condition} condition
 * @returns {Promise<boolean>}
 */
async function switchCheck(condition) {
  const switchIds = condition.switchIds ?? singleton(condition.switchId);
  const switchValues = condition.switchValues ?? singleton(condition.switchValue);

  for (const [i, swID] of switchIds.entries()) {
    const value = await getSwitch(swID);
    if (value !== switchValues[i]) return false;
  }
  
  return true;
}

/**
 * @param {Condition} condition
 * @returns {Promise<boolean>}
 */
async function variableCheck(condition) {
  const varIds = condition.varIds ?? singleton(condition.varId);
  const varValues = condition.varValues ?? singleton(condition.varValue);
  const varValues2 = [condition.varValue2];
  const ops = condition.varOps ?? singleton(condition.varOp);

  for (const [i, varID] of varIds.entries()) {
    const value = await getVariable(varID);
    const condValue = varValues[i];
    const condValue2 = varValues2[i];

    let ok;
    switch (ops[i]) {
      case '=':
        ok = value === condValue;
        break;
      case '<':
        ok = value < condValue;
        break;
      case '>':
        ok = value > condValue;
        break;
      case '<=':
        ok = value <= condValue;
        break;
      case '>=':
        ok = value >= condValue;
        break;
      case '!=':
        ok = value !== condValue;
        break;
      case '>=<':
        ok = condValue < value && value < condValue2;
        break;
    }

    if (!ok) return false;
  }

  return true;
}

/**
 * @param {Condition} condition
 */
async function conditionTriggered(condition) {
  console.log('[yno-ap-client] condition triggered: ', condition);

  // the order of these two is dynamic, so this is done a little weirdly
  if (condition.varTrigger) {
    if (!(await variableCheck(condition))) return false;
    if (!(await switchCheck(condition))) return false;
  } else {
    if (!(await switchCheck(condition))) return false;
    if (!(await variableCheck(condition))) return false;
  }

  if (!checkConditionCoords(condition)) return false;

  markConditionAsComplete(condition);
}

/**
 * for things that start listening on map load
 * @param {Condition} condition
 */
async function passiveCheckCondition(condition) {
  const values = condition.values ?? singleton(condition.value);
  if (condition.trigger === 'event' || condition.trigger === 'eventAction') {
    while (true) {
      await Promise.any(values.map(value =>
        waitForEvent(parseInt(value), condition.trigger === 'eventAction')
      ));
      const success = await checkCondition(condition, condition.trigger, values[0]);
      if (success) break;
    }
  } else if (condition.trigger === 'picture') {
    while (true) {
      await Promise.any(values.map(value =>
        waitForPicture(value)
      ));
      const success = await checkCondition(condition, condition.trigger, values[0]);
      if (success) break;
    }
  } else if (!condition.trigger) {
    if ((condition.switchId || condition.switchIds) && !condition.varTrigger) {
      const switchId = condition.switchIds?.[0] ?? condition.switchId;

      trackSwitch(switchId, !condition.switchDelay);
      while (true) {
        await waitForSwitchChange(switchId);
        const success = await conditionTriggered(condition);
        if (success) break;
      }
    } else if (condition.varId || condition.varIds) {
      const varId = condition.varIds?.[0] ?? condition.varId;
      
      while (true) {
        await waitForVariableChange(varId);
        const success = await conditionTriggered(condition);
        if (success) break;
      }
    } else {
      await conditionTriggered(condition);
    }
  }
}

/**
 * for event-caused things that do not only get transmitted because we asked the
 * client to transmit it
 * @param {Condition} condition
 * @param {TriggerType} trigger
 * @param {number | string} [value]
 */
async function checkCondition(condition, trigger, value) {
  if (condition.trigger !== trigger) return;

  const checkValues = condition.values ?? singleton(condition.value);
  const valueMatched =
    checkValues.length === 0 ||
    checkValues.some(condValue => condValue === value);

  if (!valueMatched) return;

  return await conditionTriggered(condition);
}

/**
 * @param {number} mapId
 * @returns {Condition[]}
 */
function getRelevantConditions(mapId) {
  return locations
    .flatMap(location => location.conditions ?? singleton(location.condition))
    .filter(condition => !condition.map || condition.map === mapId)
    .filter(condition =>
      shouldAlwaysListenLocation(condition.parent) ||
      !(
        isConditionComplete(condition) ||
        isLocationChecked(condition.parent.name)
      )
    );
}

/**
 * @param {number} mapId
 * @param {TriggerType} trigger 
 * @param {string} [value]
 */
export function processTrigger(mapId, trigger, value) {
  if (!isSessionValid()) return;
  const conds = getRelevantConditions(mapId);
  //console.log(`[yno-ap-client] processing trigger ${trigger}; relevant conditions: `, conds);
  Promise.all(conds.map(cond => checkCondition(cond, trigger, value)));
}

export function handleMapSwitch(mapId) {
  if (!isSessionValid()) return;
  const conds = getRelevantConditions(mapId);
  console.log(`[yno-ap-client] map${mapId.toString().padStart(4, '0')} relevant conditions: `, conds);
  Promise.all(conds.map(cond => passiveCheckCondition(cond)));
}