import esbuild from 'esbuild'
import globImport from 'esbuild-plugin-glob-import'
import fs from 'node:fs/promises';

/**
 * @type {import('esbuild').BuildOptions}
 */
const config = {
  entryPoints: [ 'src/index.user.js' ],
  outdir: 'dist/',
  bundle: true,
  banner: { js: await fs.readFile('src/index.header.js', 'utf8') },
  plugins: [
    globImport()
  ],

  logLevel: 'info',
};

if (process.argv.includes('--watch')) {
  const ctx = await esbuild.context(config);
  await ctx.watch();
} else {
  await esbuild.build(config);
}
