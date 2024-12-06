# Official OdeServer Python API's Client

## Getting Started & Usage

1. Installation:

- Use Poetry:
    ```sh
    $ poetry add odecloud
    ```
- Or, use Pip:
    ```sh
    $ pip install odecloud
    ```

2. Instantiate your connection to OdeCloud's API:

- If you don't know your client credentials:
    ```py
    from odecloud.api.connection import Api

    api = Api('https://server.odecloud.app/api/v1') # All API calls will be made to this domain.
    api.login('your-email@here.com', 'your_password', "your_app_url")
    ```

- If you already know your client credentials:
    ```py
    from odecloud.api.connection import Api
    
    api = Api(
        base_url='https://server.odecloud.app/api/v1', # All API calls will be made to this domain
        client_key='YOUR CLIENT KEY',
        client_secret='YOUR CLIENT SECRET',
    )
    ```

3. Now, any calls can be made to OdeCloud's API. Examples below:
    ```py
    api.messages(message_id).get(origin="the_app_you_are_sending_from") # GET /api/v1/messages/message_id?origin=odesocial
    api.comments.post(data=expected_payload) # POST /api/v1/comments/
    api.comments(random_comment_id).patch(data=expected_payload) # PATCH /api/v1/comments/random_comment_id/
    api.comments(random_comment_id).delete() # DELETE /api/v1/comments/random_comment_id/
    ```
Happy coding!

## Publishing to PyPI

1. On the root of the directory, open up **pyproject.toml**
2. Bump the __version__ by the following guideline:
    - Our version numbering follows **Major.Minor.Patch** (e.g. 2.10.1)
        - **Major**: Stable release.
        - **Minor**: Incremental changes--including new API, remove API, or change of behavior of the API.
        - **Patch**: Small efficient changes--including a fixed to a bug.
    - **Note**: in regards to Patch if the old functionality was always erroneous, then it will be considered a Patch.
3. Publish a new tag on the repository by going to https://gitlab.com/odetech/python_odecloud/-/tags/new.
    - **Note**: make sure that the "Tag Name" is an exact match to the version inside `pyproject.toml` on step #2.
    - In regards to the "Release notes": we encourage detail and consistent format in order for other developers to understand the new version update.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)