# fates 🔮

A robust, fully-typed, and async-ready Result pattern implementation for Python.

`fates` brings expressive, functional error handling to Python, completely removing the need for defensive `try/except` blocks. It helps you build predictable pipelines with absolute type safety for both synchronous and asynchronous operations.

---

## ✨ Features

- **🛡️ 100% Type Safe:** Full `mypy` / `pyright` compliance using generic protocols and `TypeVar` covariance.
- **⚡ Async Native:** First-class support for asynchronous mapping and monadic binding.
- **🧩 Zero Dependencies:** Lightweight and clean, relying only on standard library primitives (and `typing_extensions` for older Python versions).

---

## 🚀 Installation

```bash
pip install fates
```

---

## 📖 Quick Start

### Synchronous Usage

```python
from fates import Result, Ok, Err

def divide(a: int, b: int) -> Result[float, str]:
    if b == 0:
        return Err("Cannot divide by zero")
    return Ok(a / b)

# Monadic binding and mapping
result = (
    divide(10, 2)
    .map(lambda x: x * 2)
    .unwrap_or(0.0)
)
print(result)  # Output: 10.0
```

### Asynchronous Pipelines

`fates` shines when working with async databases or HTTP clients. Use `amap` and `abind` to pipe async operations seamlessly.

```python
import asyncio
from fates import Ok, Err, Result

async def fetch_user_id(username: str) -> Result[int, str]:
    # Simulating async DB call
    await asyncio.sleep(0.1)
    return Ok(42) if username == "admin" else Err("User not found")

async def get_user_role_async(user_id: int) -> Result[str, str]:
    await asyncio.sleep(0.1)
    return Ok("superuser")

async def main():
    # Chain async functions using abind
    pipeline = await fetch_user_id("admin").abind(get_user_role_async)
    
    print(pipeline)  # Output: Ok('superuser')
    print(pipeline.unwrap())  # Output: superuser

asyncio.run(main())
```

---

## 🛠️ API Reference

### Extracting Values

- `.unwrap()` — Returns the success value or raises an `UnwrapError`.
- `.unwrap_or(default)` — Returns the success value or a fallback value.
- `.unwrap_err()` — Returns the error value or raises an `UnwrapError`.
- `.expect(note)` — Returns the success value or crashes with a custom message.

### Transforming Results

- `.map(mapper)` — Transforms the success value inside `Ok`.
- `.map_err(mapper)` — Transforms the error value inside `Err`.
- `.bind(binder)` — Monadic bind. Chains another operation that returns a `Result`.
- `.catch(binder)` — Recovers from an error by returning an alternative `Result`.
- `.resolve(mapper)` — Merges both paths into a single success-type value.

### Async Operations

- `.amap(async_mapper)` — Asynchronously transforms the success value.
- `.amap_err(async_mapper)` — Asynchronously transforms the error value.
- `.abind(async_binder)` — Asynchronously chains another operation returning a `Result`.

---

## ⚖️ License

This project is licensed under the [MIT License](LICENSE).
