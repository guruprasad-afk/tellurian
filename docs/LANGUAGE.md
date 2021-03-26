# Syntax for writing .yaml files

- *All yaml files should start with the `actions` attribute*

```
actions:
    - resource:
    .
    .
    .
```

The actions specify the tasks to be executed.
It contains an array of resources and their respective type of action to be performed

**A yaml file must contain the actions attribute with atleast one resource attribute**

---

- *Each action will have the `resource` tag to specify the kind of resource on which on action is to be performed*

```
 - resource: DO_DOMAIN
   .
   .

```

The possible values are 
1. [DO_DOMAIN][link to DO_DOMAIN]
2. [DO_DROPLET][link to DO_DROPLET]
3. [DO_DNS_RECORD][link to DO_DNS_RECORD]

---

- *An action should have a `identifier` attribute which specifies the name of the current action*

```
- resource: DO_DOMAIN
  type: CREATE
  identifer: Create example domain
  .

```

It is not necessary to include the identifier for every action
Two actions can also have the same identifier, but this is not recommended.

---

- *The `properties` attribute of each action determines the properties of the resource that are going to be used to perform the action*

```
- resource: DO_DOMAIN
  type: CREATE
  properties:
   name: example.com

```
The properties will differ based on the resource and the type of action being performed

---

[link to DO_DOMAIN]: ../docs/DOMAIN.md
[link to DO_DROPLET]: ../docs/DROPLET.md
[link to DO_DNS_RECORD]: https://google.com
