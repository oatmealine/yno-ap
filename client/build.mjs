import esbuild from 'esbuild';
import fs from 'node:fs/promises';
import { join } from 'node:path';

const locationImporter = {
  name: 'location-importer',
  setup(build) {
    build.onResolve({ filter: /^@locations$/ }, args => ({
      path: args.path,
      namespace: 'location-importer-ns',
    }));

    build.onLoad({ filter: /.*/, namespace: 'location-importer-ns' }, async args => {
      let data = [];

      const locationsPath = join('.', 'locations');
      for (const category of await fs.readdir(locationsPath)) {
        const categoryPath = join(locationsPath, category);
        for (const filename of await fs.readdir(categoryPath)) {
          const filePath = join(categoryPath, filename);

          if (!filename.endsWith('.json'))
            continue;

          const json = await fs.readFile(filePath, 'utf8');
          const location = JSON.parse(json);

          location.filename = filename.replace('.json', '');
          for (const [i, condition] of Object.entries(location.conditions ?? [location.condition])) {
            condition.identifier = `${filename.replace('.json', '')}/${i}`;
          }

          data.push(location);
        }
      }

      return {
        contents: JSON.stringify(data),
        loader: 'json',
      } 
    });
  },
}

/**
 * @type {import('esbuild').BuildOptions}
 */
const config = {
  entryPoints: [ 'src/index.user.js' ],
  outdir: 'dist/',
  bundle: true,
  banner: { js: await fs.readFile('src/index.header.js', 'utf8') },
  plugins: [
    locationImporter,
  ],

  logLevel: 'info',
};

if (process.argv.includes('--watch')) {
  const ctx = await esbuild.context(config);
  await ctx.watch();
} else {
  await esbuild.build(config);
}
