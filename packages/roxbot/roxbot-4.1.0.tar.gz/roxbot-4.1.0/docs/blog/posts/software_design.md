---
draft: false
date: 2023-12-01
categories:
  - dev-tips
authors:
  - jev
---

# Solid Software Design Principles for Robotics Developers

My journey as a robotics developer began during my Physics studies. There was a significant shift from initially writing complex and chaotic code to my current effective use of various software design patterns and practices. This change has been crucial for building scalable and reliable software for autonomous machines. Like many robotics enthusiasts, my journey didn't start with a Computer Science degree; I learned programming through hands-on experience in the field.

In this post, I aim to share the key design principles that guide me every day. These principles have enabled me to independently create advanced robotics software, making the entire development process more manageable and efficient.

<!-- more -->

Here are the guiding principles of software development, with the most crucial ones listed first:

1. **KISS (Keep It Simple, Stupid)**: Embrace simplicity. Avoid over-complicating systems with unnecessary complexities, as this can hinder understanding, maintenance, and scalability.

2. **Less Code Equals Fewer Problems**: The more code you have, the more bugs, tests, and maintenance it requires. Strive for minimal code to achieve a system that's easier to understand and maintain. This principle complements *YAGNI*.

3. **DRY (Don't Repeat Yourself)**: Avoid code duplication. Ensure each piece of knowledge or logic exists only once in your codebase, reducing redundancy and simplifying maintenance.

4. **YAGNI (You Aren’t Gonna Need It)**: Guard against over-engineering. Add features only when they're necessary, rather than preemptively implementing "just in case" functionalities.

5. **Code Modularity**: Break down your codebase into smaller, manageable modules or components. Each module should handle a specific functionality, allowing for independent development and testing. Enhancing this approach with containerization technologies like Docker, you can create microservices with clear interfaces and separated subsystems.

6. **Principle of Least Astonishment (POLA)**: Ensure your software acts in predictable and consistent ways. Functions, classes, and modules should do exactly what their names imply, avoiding surprises for users and developers alike.

7. **SOLID Principles**: These five principles aim to make software design more understandable, flexible, and maintainable:
    - **Single Responsibility Principle (SRP)**: Each class should have one and only one reason to change, focusing on a single aspect of functionality.
    - **Open/Closed Principle (OCP)**: Design software entities (classes, modules, functions, etc.) to be open for extension but closed for modification.
    - **Liskov Substitution Principle (LSP)**: Objects of a superclass should be replaceable with objects of its subclasses without affecting program correctness.
    - **Interface Segregation Principle (ISP)**: Avoid forcing clients to depend on methods they don't use. Prefer smaller, specific interfaces over large, general-purpose ones.
    - **Dependency Inversion Principle (DIP)**: High-level modules should not depend on low-level modules. Both should rely on abstractions, which, in turn, should not depend on details. Instead, details should depend on abstractions.


I'll illustrate the use of `SOLID` principles with a practical toy example:


```python
--8<-- "examples/snippets/design_principles.py"
```

...


I hope this practical toy example has illuminated how the SOLID principles can be applied in real-world scenarios.

Happy coding!
