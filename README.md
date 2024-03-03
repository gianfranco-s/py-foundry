Python shield for cf-cli v8.

Will move to use the API in the future.

## How to use
1. Install [`cf cli`](https://docs.cloudfoundry.org/cf-cli/install-go-cli.html)
2. (Optional) Install dependencies with
   ```
   $ poetry install
   ```
3. Create credentials file following `cf_creds_template.json`
4. The library follows the basic command list from `cf cli`
5. There are some helpful classes in cf_utils.py


## To do
GETTING STARTED:
   - [ ] help                                   Show help
   - [ ] version                                Print the version
   - [x] login                                  Log user in
   - [ ] logout                                 Log user out
   - [ ] passwd                                 Change user password
   - [x] target                                 Set or view the targeted org or space

   - [x] api                                    Set or view target api url
   - [ ] auth                                   Authenticate non-interactively

APPS:
   - [x] apps                                   List all apps in the target space
   - [ ] app                                    Display health and status for an app
   - [x] create-app                             Create an Application in the target space

   - [ ] push                                   Push a new app or sync changes to an existing app
   - [ ] scale                                  Change or view the instance count, disk space limit, memory limit, and log rate limit for an app
   - [ ] delete                                 Delete an app
   - [ ] rename                                 Rename an app

   - [ ] cancel-deployment                      Cancel the most recent deployment for an app. Resets the current droplet to the previous deployment's droplet.

   - [ ] start                                  Start an app
   - [ ] stop                                   Stop an app
   - [ ] restart                                Stop all instances of the app, then start them again.
   - [ ] stage-package                          Stage a package into a droplet
   - [ ] restage                                Stage the app's latest package into a droplet and restart the app with this new droplet and updated configuration (environment variables, service bindings, buildpack, stack, etc.).
   - [ ] restart-app-instance                   Terminate, then instantiate an app instance

   - [ ] run-task                               Run a one-off task on an app
   - [ ] tasks                                  List tasks of an app
   - [ ] terminate-task                         Terminate a running task of an app

   - [ ] packages                               List packages of an app
   - [ ] create-package                         Uploads a Package

   - [ ] droplets                               List droplets of an app
   - [ ] set-droplet                            Set the droplet used to run an app
   - [ ] download-droplet                       Download an application droplet

   - [ ] events                                 Show recent app events
   - [ ] logs                                   Tail or show recent logs for an app

   - [x] env                                    Show all env variables for an app
   - [x] set-env                                Set an env variable for an app
   - [ ] unset-env                              Remove an env variable from an app

   - [ ] stacks                                 List all stacks (a stack is a pre-built file system, including an operating system, that can run apps)
   - [ ] stack                                  Show information for a stack (a stack is a pre-built file system, including an operating system, that can run apps)

   - [ ] copy-source                            Copies the source code of an application to another existing application and restages that application
   - [ ] create-app-manifest                    Create an app manifest for an app that has been pushed successfully

   - [ ] get-health-check                       Show the type of health check performed on an app
   - [ ] set-health-check                       Change type of health check performed on an app's process
   - [ ] enable-ssh                             Enable ssh for the application
   - [ ] disable-ssh                            Disable ssh for the application
   - [ ] ssh-enabled                            Reports whether SSH is enabled on an application container instance
   - [ ] ssh                                    SSH to an application container instance

SERVICES:
   - [ ] marketplace                            List available offerings in the marketplace
   - [x] services                               List all service instances in the target space
   - [ ] service                                Show service instance info

   - [x] create-service                         Create a service instance
   - [ ] update-service                         Update a service instance
   - [ ] upgrade-service                        Upgrade a service instance to the latest available version of its current service plan
   - [ ] delete-service                         Delete a service instance
   - [ ] rename-service                         Rename a service instance

   - [x] create-service-key                     Create key for a service instance
   - [ ] service-keys                           List keys for a service instance
   - [x] service-key                            Show service key info
   - [x] delete-service-key                     Delete a service key

   - [ ] bind-service                           Bind a service instance to an app
   - [ ] unbind-service                         Unbind a service instance from an app

   - [ ] bind-route-service                     Bind a service instance to an HTTP route
   - [ ] unbind-route-service                   Unbind a service instance from an HTTP route

   - [x] create-user-provided-service           Make a user-provided service instance available to CF apps
   - [ ] update-user-provided-service           Update user-provided service instance

   - [ ] share-service                          Share a service instance with another space
   - [ ] unshare-service                        Unshare a shared service instance from a space

ORGS:
   - [ ] orgs                                   List all orgs
   - [ ] org                                    Show org info

SPACES:
   - [ ] spaces                                 List all spaces in an org
   - [ ] space                                  Show space info

DOMAINS:
   - [ ] domains                                List domains in the target org

ROUTES:
   - [ ] routes                                 List all routes in the current space or the current organization
   - [ ] route                                  Display route details and mapped destinations

   - [ ] create-route                           Create a route for later use
   - [ ] check-route                            Perform a check to determine whether a route currently exists or not
   - [ ] map-route                              Map a route to an app
   - [ ] unmap-route                            Remove a route from an app
   - [ ] delete-route                           Delete a route

   - [ ] delete-orphaned-routes                 Delete all orphaned routes in the currently targeted space (i.e. those that are not mapped to an app or service instance)

   - [ ] update-destination                     Updates the destination protocol for a route

   - [ ] share-route                            Share a route in between spaces
   - [ ] unshare-route                          Unshare an existing route from a space

   - [ ] move-route                             Assign a route to a different space

USER ADMIN:
   - [ ] create-user                            Create a new user
   - [ ] delete-user                            Delete a user

   - [ ] org-users                              Show org users by role
   - [ ] set-org-role                           Assign an org role to a user
   - [ ] unset-org-role                         Remove an org role from a user

   - [ ] space-users                            Show space users by role
   - [ ] set-space-role                         Assign a space role to a user
   - [ ] unset-space-role                       Remove a space role from a user

SPACE ADMIN:
   - [ ] space-quotas                           List available space quotas
   - [ ] space-quota                            Show space quota info

   - [ ] create-space-quota                     Define a new quota for a space
   - [ ] update-space-quota                     Update an existing space quota
   - [ ] delete-space-quota                     Delete a space quota

   - [ ] set-space-quota                        Assign a quota to a space
   - [ ] unset-space-quota                      Unassign a quota from a space

ADVANCED:
   - [ ] curl                                   Executes a request to the targeted API endpoint
   - [ ] config                                 Write default values to the config
   - [ ] oauth-token                            Display the OAuth token for the current session and refresh the token if necessary
   - [ ] ssh-code                               Get a one time password for ssh clients


## Won't develop
- ORGS:
   create-org
   delete-org
   rename-org

- SPACES:
   create-space
   delete-space
   rename-space
   apply-manifest

   allow-space-ssh
   disallow-space-ssh
   space-ssh-allowed

- DOMAINS:
   create-private-domain
   delete-private-domain

   create-shared-domain
   delete-shared-domain

   router-groups

- ORG ADMIN
- SERVICE ADMIN
- SECURITY GROUP
- ENVIRONMENT VARIABLE GROUPS
- ISOLATION SEGMENTS
- FEATURE FLAGS
- METADATA
- ADD/REMOVE PLUGIN REPOSITORY
- ADD/REMOVE PLUGIN
- ENVIRONMENT VARIABLES
- INSTALLED PLUGIN COMMANDS
- EXPERIMENTAL COMMANDS
- NETWORK POLICIES
- BUILDPACKS
