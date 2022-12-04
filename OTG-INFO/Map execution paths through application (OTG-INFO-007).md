## Summary

Before commencing security testing, understanding the structure of the application is paramount. Without a thorough understanding of the layout of the application, it is unlkely that it will be tested thoroughly.

## Test Objectives

Map the target application and understand the principal workflows.

## How to Test

There are several ways to approach the testing and measurement of code coverage:

- Path - test each of the paths through an application that includes combinatorial and boundary value analysis testing for each decision path. While this approach offers thoroughness, the number of testable paths grows exponentially with each decision
branch.
- Data flow (or taint analysis) - tests the assignment of variables via external interaction (normally users). Focuses on mapping the flow, transformation and use of data throughout an application.
- Race - tests multiple concurrent instances of the application manipulating the same data.

The trade off as to what method is used and to what degree each method is used should be negotiated with the application owner. Simpler approaches could also be adopted, including asking the application owner what functions or code sections they are particularly concerned about and how those code segments can be reached.

## Automatic Spidering

- Zed Attack Proxy (ZAP)

ZAP offers the following automatic spidering features, which can be selected based on the tester’s needs:

- Spider Site - The seed list contains all the existing URIs already found for the selected site.
- Spider Subtree - The seed list contains all the existing URIs already
found and present in the subtree of the selected node.
- Spider URL - The seed list contains only the URI corresponding to
the selected node (in the Site Tree).
- Spider all in Scope - The seed list contains all the URIs the user has
selected as being ‘In Scope’.
