# Documentation for DO_DROPLET

## Description

The DO_DROPLET resource is used to create one or more droplets. 

## Properties

For the DO_DROPLET resource, the following properties are to be specified

#### Required Properties

**1. `names`**

*type*: _Array_

An array of human human-readable strings you wish to use when displaying the Droplet name.

Example: `names: ["droplet_example1", "droplet_example2"]`

**2. `region`**

type: _String_

The unique slug identifier for the region that you wish to deploy in.

Example: `region: "nyc3"`

**3. `size`**

*type*: _String_

The unique slug identifier for the size that you wish to select for this Droplet.

Example: `size: "s-1vcpu-1gb"`

**4. `image`**

*type*: _String_

The image ID of a public or private image, or the unique slug identifier for a public image. This image will be the base image for your Droplet.

Example: `image: "ubuntu-16-04-x64"`

---

#### Optional Properties

**5. `ssh_keys`**

*type*: _String_

An array containing fingerprints of the SSH keys that you wish to embed in the Droplet's root account upon creation. By default, no ssh keys are added when creating the droplet

Example: `ssh_keys: ["15:28:xx:xx:5a:98:xx:xx:xx:2b:89:xx:70:xx:xx:11"]`

**6. `backups`**

*type*: _Boolean_

A boolean indicating whether automated backups should be enabled for the Droplet. Defaults to false. 

Example: `backups: true`

**7. `ipv6`**

*type*: _Boolean_

A boolean indicating whether IPv6 is enabled on the Droplet.Defaults to false

Example: `ipv6: false`

**8. `vpc_uuid`**

*type*: _String_

A string specifying the UUID of the VPC to which the Droplet will be assigned. If excluded, the Droplet will be assigned to your account's default VPC for the region.

Example: `vpc_uuid: "default-nyc1"`

**9. `user_data`**

*type*: _String_

A string containing 'user data' which may be used to configure the Droplet on first boot, often a 'cloud-config' file or Bash script. It must be plain text and may not exceed 64 KiB in size.

**10. `monitoring`**

*type*: _Boolean_

A boolean indicating whether to install the DigitalOcean agent for monitoring.Defaults to false

Example: `monitoring: false`

**11. `tags`**

*type*: _Array_

A flat array of tag names as strings to apply to the Droplet after it is created. Tag names can either be existing or new tags.

Example: `tags: ["web", "server", "dev"]`


