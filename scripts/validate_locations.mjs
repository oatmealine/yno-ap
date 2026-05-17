import * as z from 'zod';
import * as fs from 'node:fs/promises';
import { join } from 'node:path';
import { execSync } from 'node:child_process';

const Op = z.enum(['=', '<', '>', '<=', '>=', '!=', '>=<']);
const Trigger = z.enum(['', 'event', 'eventAction', 'picture', 'coords', 'teleport', 'prevMap']);

const Condition = z.intersection(
  z.object({
    map: z.optional(z.int()),
  }),
  z.union([
    z.intersection(
      z.xor([
        z.object({
          switchId: z.int(),
          switchValue: z.boolean(),
        }),
        z.object({
          switchIds: z.array(z.int()),
          switchValues: z.array(z.boolean()),
        }),
      ]),
      z.object({
        switchDelay: z.optional(z.boolean()),
      }),
    ),
    
    z.intersection(
      z.xor([
        z.object({
          varId: z.int(),
          varValue: z.int(),
          varValue2: z.optional(z.int()),
          varOp: z.optional(Op),
        }),
        z.object({
          varIds: z.array(z.int()),
          varValues: z.array(z.int()),
          varOps: z.optional(z.array(Op)),
        }),
      ]),
      z.object({
        varDelay: z.optional(z.boolean()),
        varTrigger: z.optional(z.boolean()),
      }),
    ),
    
    z.intersection(
      z.object({
        trigger: Trigger,
      }),
      z.xor([
        z.object({
          value: z.optional(z.string()),
        }),
        z.object({
          values: z.optional(z.array(z.string())),
        }),
      ]),
    ),

    z.object({
      mapX1: z.optional(z.int()),
      mapY1: z.optional(z.int()),
      mapX2: z.optional(z.int()),
      mapY2: z.optional(z.int()),

      timeTrial: z.optional(z.boolean()),
    }),
  ]),
);

const Location = z.intersection(
  z.object({
    name: z.string(),
  }),
  z.xor([z.object({
    condition: Condition,
  }), z.object({
    conditions: z.array(Condition),
    conditionsCount: z.optional(z.int()),
  })])
);

let warnings = 0;
let errors = 0;

function warn(msg) {
  console.log(`[WARN] ${msg}`);
  warnings++;
}
function error(msg) {
  console.log(`[ERROR] ${msg}`);
  errors++;
}

const apworldPath = join(import.meta.dirname, '../apworld');

const pythonOutput = execSync(`python3 -c "import json
import sys
sys.path.append('${apworldPath.replaceAll('\'', '\\\'')}')
from data import locations
print(json.dumps([location.name for location in locations]))"`);

const knownLocations = JSON.parse(pythonOutput.toString('utf8'));

const locationsPath = join(import.meta.dirname, '../client/locations/');

const rootDirs = await fs.readdir(locationsPath);
for (const dir of rootDirs) {
  const dirPath = join(locationsPath, dir);
  const stat = await fs.stat(dirPath);
  if (!stat.isDirectory()) {
    warn(`locations/${dir} is not a directory; this file will be ignored by the client`);
    continue;
  }

  const subDirs = await fs.readdir(dirPath);
  for (const subDir of subDirs) {
    const subDirPath = join(dirPath, subDir);
    const stat = await fs.stat(subDirPath);
    if (stat.isDirectory()) {
      warn(`locations/${dir}/${subDir} is a directory; its contents will be ignored by the client`);
      continue;
    }

    if (subDir.endsWith('.json') && stat.isFile()) {
      const filename = `locations/${dir}/${subDir}`;
      const content = await fs.readFile(subDirPath, 'utf8');
      let parsed;
      try {
        parsed = JSON.parse(content);
      } catch(err) {
        error(`${filename}: ${err}`);
        continue;
      }
      
      const res = Location.safeParse(parsed);
      if (res.success) {
        const data = res.data;

        let hasWarnings;

        if (!knownLocations.includes(data.name)) {
          hasWarnings = true;
          warn(`${filename}: unknown location \`${data.name}\``);
        }

        const conditions = data.conditions ?? [data.condition];
        for (const condition of conditions) {
          if (condition.map === undefined) {
            hasWarnings = true;
            warn(`${filename}: omitting \`map\` results in checks done in every map, use with caution`);
          }
        }

        if (!hasWarnings)
          console.log(`${filename}: OK`);
      } else {
        error(`${filename}: parse error`);
        console.log(z.prettifyError(res.error));
      }
    }
  }
}

console.log();
console.log(`${errors} error${errors === 1 ? '' : 's'}, ${warnings} warning${warnings === 1 ? '' : 's'}`);