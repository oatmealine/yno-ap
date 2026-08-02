console.log('[yno-ap-client] hello from yno AP client \\o/');

if (location.hostname === 'explorer.yume.wiki') {
  import('./entrypoints/explorer.js');
} else {
  import('./entrypoints/yno.js');
}