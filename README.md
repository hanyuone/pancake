# Pancake

**Pancake** is a minimalistic stack-based language, with a few basic builtins and a world of possibilities.

## How to run

Download the project and run `python main.py filename`, where `filename` is the location of your file with a `.pan` extension. You can try out some of the example files in the `/example` folder!

- `arithmetic.pan`: Basic arithmetic functions
- `curry.pan`: Demonstrates closures and currying
- `factorial.pan`: Basic factorial function/recursion
- `hello.pan`: "Hello, World!"
- `import.pan`: Imports stuff from `list.pan` and runs code from there
- `list.pan`: A bunch of first-class list comprehension functions, including `map` and `filter`

## Writing Pancake code

In Pancake, there are a couple of data types:

- Integers (`5`, `3`, `-15`)
- Floats (`3.14`)
- Strings (`"Hello, World!"`)
- Lists (`[ 1 2 3 4 5 ]`)
- Functions (`{ n : n 1 + }`, all arguments are before the `:`)

Whenever you write a piece of data down in your Pancake code, it gets **automatically pushed onto the stack**.

```
5
# 5 gets pushed onto the stack, so the stack right now is [5]
3
# 3 gets pushed on, so the stack from top to bottom is [5, 3]
"Hello"
# A string gets pushed on, stack = [5, 3, "Hello"]
```

We can declare variables using `={name}`, where `{name}` is the name of the variable. This pops the topmost value from the stack and sets it to that name, so whenever you reference that name again, that value gets pushed instead.

```
5 =n
# We push 5 onto the stack, then we pop it from the stack and set n to be equal to 5
3 n
# The stack is empty, so we push 3 and then n = 5, so the stack is now [3, 5]
+
# + is a builtin function that takes the top two values of the stack, adds them
# together and pushes that value to the stack, so the stack is now [8] (3 + 5 = 8)
```

If we want a piece of code that we can execute more than once, we can write **functions** using `{}`:

```
{ n : n 1 + } =>inc
```

In the above function (called `inc`), the function takes one value off the stack and declares it to be `n`. It then pushes `n` to the stack alongside a `1`, adds them together to put `n + 1` onto the stack, which is the increment function. The `=>` notation tells the interpreter that we want `inc` to be a function, and we can now use `inc` like this:

```
5 inc print # => 6
# Pushes the increment of 5 to the stack, which is 6, and prints it out
# (which also pops it from the stack)
```

We can also just have "raw" (lambda) functions on the stack, since they get pushed automatically, and we can run these functions by using the `execute` keyword:

```
5 { n : n 1 + } execute print # => 6
# The stack looks like [5, { n : n 1 + }], with the execute keyword
# the function is popped from the top of the stack and executed with the
# rest of the stack, in this case 5
```

Functions are ubiquitous in Pancake - in fact, control flow statements like `if` also technically use functions, ones without any arguments:

```
{ n : n 0 eq } =>zero?
0 =index
{: "Index is not 0" print } {: "Index is 0" print } index zero? if # => "Index is 0" 
```

## Issues and PRs

If you find any errors within the compiler (i.e. something doesn't work as expected, a bug exists) or you want to implement a new feature, be sure to open an issue or pull request in the Github project!
