# Documentation for DO_DNS_RECORD

## Description

The Domain record resource is used to set or retrieve information about the individual DNS records configured for a domain.

## Properties

For the DO_DNS_RECORD resource, the following properties can be specified

#### Required Properties

**1. `domain`**

type: _String_

Specifies the domain to add the record
This property is required for all dns record types

Example: `domain: "example.com"`

**2. `type`**

type: _String_

Specifies the record type. The possible values are A, AAAA, CNAME

Example: `type: "A"`

**3. `name`**

type: _String_

The host name, alias, or service being defined by the record. For example if this name is set to "api" then the domain record would be added for api.domain.com

Example: `name: "developer"`

**4. `data`**

type: _String_

Variable data depending on record type. For example, the "data" value for an A record would be the IPv4 address to which the domain will be mapped. For a CAA record, it would contain the domain name of the CA being granted permission to issue certificates.

Example: `name: "1.2.3.4"`
