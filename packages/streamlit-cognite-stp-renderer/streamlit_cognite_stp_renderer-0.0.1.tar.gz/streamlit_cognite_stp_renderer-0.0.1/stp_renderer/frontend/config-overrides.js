const USE_FIX = true;

module.exports = function override(config, env) {
  if (!USE_FIX) {
    return config;
  }

  // Update the oneOf rules to exclude certain modules
  config.module.rules[1].oneOf = config.module.rules[1].oneOf.map((rule) => {
    if (rule.type !== 'asset/resource') {
      return rule;
    }

    return {
      ...rule,
      exclude: [...rule.exclude, /node_modules(\\|\/)three/],
    };
  });

  // Add a dedicated loader for WASM at the beginning of oneOf rules
  const wasmLoader = {
    test: /\.wasm$/,
    type: 'asset/inline'
  };

  // Ensure we add it to the correct location in the rules
  const oneOfRule = config.module.rules.find((rule) => Array.isArray(rule.oneOf));
  if (oneOfRule) {
    oneOfRule.oneOf.unshift(wasmLoader);
  } else {
    // Fallback if the structure is unexpected
    config.module.rules.push(wasmLoader);
  }

  // Add resolve fallback for Node.js core modules
  config.resolve.fallback = {
    ...config.resolve.fallback,
    fs: false,
    perf_hooks: false,
    os: false,
    path: false,
    worker_threads: false,
    crypto: false,
    stream: false,
  };

  return config;
};
