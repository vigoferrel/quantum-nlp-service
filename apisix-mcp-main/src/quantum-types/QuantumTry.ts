/**
 * Implementación de Try para manejo seguro de errores
 */
export class QuantumTry<E extends Error, T> {
    private constructor(
        private readonly value: T | null,
        private readonly error: E | null
    ) {}

    static Success<E extends Error, T>(value: T): QuantumTry<E, T> {
        return new QuantumTry<E, T>(value, null);
    }

    static Failure<E extends Error, T>(error: E): QuantumTry<E, T> {
        return new QuantumTry<E, T>(null, error);
    }

    static From<E extends Error, T>(fn: () => T): QuantumTry<E, T> {
        try {
            return QuantumTry.Success<E, T>(fn());
        } catch (error) {
            return QuantumTry.Failure<E, T>(error as E);
        }
    }

    isSuccess(): boolean {
        return this.error === null;
    }

    isFailure(): boolean {
        return this.error !== null;
    }

    getOrElse(defaultValue: T): T {
        return this.value ?? defaultValue;
    }

    getOrNull(): T | null {
        return this.value;
    }

    getErrorOrNull(): E | null {
        return this.error;
    }

    map<U>(fn: (value: T) => U): QuantumTry<E, U> {
        if (this.error !== null) {
            return QuantumTry.Failure(this.error);
        }
        try {
            return QuantumTry.Success(fn(this.value!));
        } catch (error) {
            return QuantumTry.Failure(error as E);
        }
    }

    flatMap<U>(fn: (value: T) => QuantumTry<E, U>): QuantumTry<E, U> {
        if (this.error !== null) {
            return QuantumTry.Failure(this.error);
        }
        try {
            return fn(this.value!);
        } catch (error) {
            return QuantumTry.Failure(error as E);
        }
    }

    fold<U>(successFn: (value: T) => U, failureFn: (error: E) => U): U {
        return this.error !== null ? failureFn(this.error) : successFn(this.value!);
    }

    recover(fn: (error: E) => T): QuantumTry<E, T> {
        if (this.error !== null) {
            try {
                return QuantumTry.Success(fn(this.error));
            } catch (error) {
                return QuantumTry.Failure(error as E);
            }
        }
        return this;
    }

    recoverWith(fn: (error: E) => QuantumTry<E, T>): QuantumTry<E, T> {
        if (this.error !== null) {
            try {
                return fn(this.error);
            } catch (error) {
                return QuantumTry.Failure(error as E);
            }
        }
        return this;
    }
}