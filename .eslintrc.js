const path = require('path')

module.exports = {
    'root': true,
    'extends': [ 'eslint:recommended', 'plugin:vue/recommended', 'plugin:import/errors', 'plugin:import/warnings' ],
    'env': {
        'browser': true,
        'node': true,
        'es6': true
    },
    'globals': {
        '__DEV__': false,
        '__TEST__': false,
        '__PROD__': false,
        'DJANGO_SETTINGS_MODULE': false,
        'GITINFO': false,
        'System': false
    },
    'settings': {
        'import/resolver': {
            'webpack': {
                'config': path.resolve('./webpack.config.eslint.js')
            }
        },
        'html/html-extensions': [ '.html', '.vue' ]
    },
    'parserOptions': {
        'parser': 'babel-eslint',
        'ecmaVersion': 2017,
        'sourceType': 'module'
    },
    'rules': {
        'indent': 'off',
        'indent-legacy': [ 'error', 4, { 'SwitchCase': 1 } ],
        'space-before-function-paren': [ 0 ],
        'operator-linebreak': [ 'error', 'before' ],
        'quotes': [ 'error', 'single', { 'allowTemplateLiterals': true } ],
        'camelcase': [ 'warn', { 'properties': 'never' } ],
        'object-curly-spacing': [ 'warn', 'always' ],
        'object-curly-newline': [ 'warn', { 'multiline': true } ],
        'array-bracket-spacing': [ 'warn', 'always' ],
        'array-element-newline': [ 'warn', {
            'minItems': 4,
            'multiline': true
        } ],
        'semi': [ 'error', 'never' ],
        'comma-dangle': [ 'error', 'never' ],
        'no-param-reassign': [ 'error', { 'props': false } ],
        'curly': [ 'error', 'multi' ],
        'max-len': [ 'warn', 120 ],
        'no-mixed-operators': [ 'error', { 'allowSamePrecedence': true } ],
        'no-empty': [ 'error' ],
        'no-console': [ 'warn', { 'allow': [ 'error', 'warn' ] } ]
    },
    'overrides': [
        {
            'files': [ '*.vue' ],
            'rules': {
                'indent': 'off',
                'max-len': [ 'warn', 180 ],
                'vue/html-indent': [ 'error', 4, {
                    'baseIndent': 1,
                    'ignores': [ 'VText' ]
                } ],
                'vue/script-indent': [ 'error', 4, {
                    'baseIndent': 1,
                    'switchCase': 1
                } ],
                'vue/attributes-order': [ 1 ],
                'vue/max-attributes-per-line': [
                    'warn',
                    {
                        'singleline': 4,
                        'multiline': {
                            'max': 3,
                            'allowFirstLine': true
                        }
                    }
                ],
                'vue/singleline-html-element-content-newline': false,
                'vue/html-closing-bracket-newline': false
            }
        }
    ]
}
