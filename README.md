# chatgpt

A [Remotion](https://remotion.dev) video project — scaffolded with `npx create-video@latest` (Hello World template).

## Commands

Install the dependencies first:

```console
npm install
```

**Start the Studio** (a live preview of your video in the browser):

```console
npm run dev
```

**Render a video** to `out/`:

```console
npx remotion render
```

You can also render a specific composition by its ID:

```console
npx remotion render HelloWorld
```

**Upgrade Remotion** to the latest version:

```console
npm run upgrade
```

## Project structure

- `src/index.ts` — registers the root component with Remotion.
- `src/Root.tsx` — declares the `<Composition>`s that appear in the Studio sidebar.
- `src/HelloWorld.tsx` — the main animated composition.
- `src/HelloWorld/` — the individual components (logo, title, subtitle).
- `remotion.config.ts` — render configuration (see the [config docs](https://remotion.dev/docs/config)).

## Learn more

- [Remotion fundamentals](https://www.remotion.dev/docs/the-fundamentals)
- [API reference](https://www.remotion.dev/docs/api)
- [Discord community](https://remotion.dev/discord)

## License

Note that for some entities a company license is needed. [Read the terms here](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md).
