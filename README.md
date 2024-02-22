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
