export function isArray(x) {
    return Array.isArray(x)
}

export function arrayize(values) {
    // return empty array if values is empty
    if (typeof values === 'undefined' || values === null)
        return []

    // return array of values, converting to array if necessary
    return isArray(values) ? values : [ values ]
}
