/**
 * Implementación de Try para manejo seguro de errores
 */
export class Try<E extends Error, T> {
    private constructor(
        private readonly value: T | null,
        private readonly error: E | null
    ) {}

    static Success<E extends Error, T>(value: T): Try<E, T> {
        return new Try<E, T>(value, null);
    }

    static Failure<E extends Error, T>(error: E): Try<E, T> {
        return new Try<E, T>(null, error);
    }

    static From<E extends Error, T>(fn: () => T): Try<E, T> {
        try {
            return Try.Success<E, T>(fn());
        } catch (error) {
            return Try.Failure<E, T>(error as E);
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

    map<U>(fn: (value: T) => U): Try<E, U> {
        if (this.error !== null) {
            return Try.Failure(this.error);
        }
        try {
            return Try.Success(fn(this.value!));
        } catch (error) {
            return Try.Failure(error as E);
        }
    }

    flatMap<U>(fn: (value: T) => Try<E, U>): Try<E, U> {
        if (this.error !== null) {
            return Try.Failure(this.error);
        }
        try {
            return fn(this.value!);
        } catch (error) {
            return Try.Failure(error as E);
        }
    }

    fold<U>(successFn: (value: T) => U, failureFn: (error: E) => U): U {
        return this.error !== null ? failureFn(this.error) : successFn(this.value!);
    }

    recover(fn: (error: E) => T): Try<E, T> {
        if (this.error !== null) {
            try {
                return Try.Success(fn(this.error));
            } catch (error) {
                return Try.Failure(error as E);
            }
        }
        return this;
    }

    recoverWith(fn: (error: E) => Try<E, T>): Try<E, T> {
        if (this.error !== null) {
            try {
                return fn(this.error);
            } catch (error) {
                return Try.Failure(error as E);
            }
        }
        return this;
    }
}