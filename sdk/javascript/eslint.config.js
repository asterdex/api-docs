export default [
  {
    files: ["src/**/*.js", "tests/**/*.js"],
    rules: {
      "no-unused-vars": ["error", { argsIgnorePattern: "^_" }],
      "no-console": "warn",
      "no-eval": "error",
      "no-implied-eval": "error",
      "no-new-func": "error",
      "prefer-const": "error",
      "no-var": "error",
      eqeqeq: "error",
      "no-throw-literal": "error",
    },
  },
];
