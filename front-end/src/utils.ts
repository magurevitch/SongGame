export function makeComparison<T>(selector: (object: T) => number | string): (a: T, b:T) => number {
    return (a, b) => selector(a) > selector(b) ? 1 : selector(b) > selector(a) ? -1 : 0;
}