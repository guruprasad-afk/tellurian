# Documentation for DO_DOMAIN

## Description

The DO_DOMAIN resource is used to add a Domain to the Digital Ocean DNS management system.

## Properties

For the DO_DOMAIN resource, the following properties can be specified

#### Required Properties

**1. `name`**

*type*: _String_

The domain name to add to the DigitalOcean DNS management interface. The name must be unique in DigitalOcean's DNS system.

Example: `name: "example.com"`

#### Optional Properties

**2. `ip_address`**

*type*: _String_

When provided, an A record will be automatically created pointing to the apex domain.

Example: `ip_address: "1.2.3.4"`

