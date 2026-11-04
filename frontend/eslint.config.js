import js from "@eslint/js";
import react from "eslint-plugin-react";
import hooks from "eslint-plugin-react-hooks";
export default [
  { ignores: ["dist/**", "node_modules/**"] },
  js.configs.recommended,
  { files: ["**/*.{js,jsx}"], languageOptions: { ecmaVersion: "latest", sourceType: "module", globals: { window: "readonly", document: "readonly", console: "readonly", fetch: "readonly", localStorage: "readonly", process: "readonly" }, parserOptions: { ecmaFeatures: { jsx: true } } }, plugins: { react, "react-hooks": hooks }, rules: { "no-unused-vars": ["warn", { argsIgnorePattern: "^_", varsIgnorePattern: "^[A-Z_]" }], "react/react-in-jsx-scope": "off", "react-hooks/rules-of-hooks": "error", "react-hooks/exhaustive-deps": "warn" } }
];
