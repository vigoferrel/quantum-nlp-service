/**
 * Implementación de Either para manejo de resultados duales
 */
export class QuantumEither<L, R> {
    private constructor(
        private readonly left: L | null,
        private readonly right: R | null
    ) {}

    static Left<L, R>(value: L): QuantumEither<L, R> {
        return new QuantumEither<L, R>(value, null);
    }

    static Right<L, R>(value: R): QuantumEither<L, R> {
        return new QuantumEither<L, R>(null, value);
    }

    isLeft(): boolean {
        return this.left !== null;
    }

    isRight(): boolean {
        return this.right !== null;
    }

    fold<T>(leftFn: (left: L) => T, rightFn: (right: R) => T): T {
        return this.left !== null ? leftFn(this.left) : rightFn(this.right!);
    }

    map<U>(fn: (right: R) => U): QuantumEither<L, U> {
        return this.right === null 
            ? QuantumEither.Left(this.left!)
            : QuantumEither.Right(fn(this.right));
    }

    flatMap<U>(fn: (right: R) => QuantumEither<L, U>): QuantumEither<L, U> {
        return this.right === null
            ? QuantumEither.Left(this.left!)
            : fn(this.right);
    }
}