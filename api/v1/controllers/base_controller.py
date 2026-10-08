"""
Base controller module.

Provides the standard CRUD handler pattern that entity-specific
controllers inherit and customize.
"""


class BaseController:
    """
    Abstract base for REST controllers.

    Subclasses must set:
      - repository_class: the BaseRepository subclass to use
      - validator_class: the BaseValidator subclass to use
      - model_class: the Persistent model class to instantiate
      - entity_name: human-readable name for messages (e.g. 'Car')
      - _model_fields: list of field names for building model instances
    """

    repository_class = None
    validator_class = None
    model_class = None
    entity_name = "Entity"
    _model_fields = []

    def __init__(self):
        """Instantiate the repository for this controller."""
        self.repository = self.repository_class()

    def list_all(self, request, response, **kwargs):
        """
        GET handler: return all items in the collection.

        :param request: Request object
        :param response: Response object
        """
        items = self.repository.get_all()
        data = [{"id": item_id, **obj.to_dict()} for item_id, obj in items]
        response.ok(data=data)

    def get_one(self, request, response, **kwargs):
        """
        GET handler: return a single item by ID.

        :param kwargs: must contain 'id'
        """
        item_id = int(kwargs.get("id"))
        obj = self.repository.get_by_id(item_id)
        if obj is None:
            response.not_found(f"{self.entity_name} with id {item_id} not found.")
            return
        response.ok(data={"id": item_id, **obj.to_dict()})

    def create(self, request, response, **kwargs):
        """
        POST handler: validate and create a new item.

        Subclasses can override _build_model() to customize
        how the model instance is created from request data.
        """
        data = request.json()

        # -- Validate request body --
        errors = self.validator_class.validate_create(data)
        if errors:
            response.bad_request(errors=errors)
            return

        # -- Build model and persist --
        obj = self._build_model(data)
        item_id = self.repository.create(obj)
        response.created(data={"id": item_id, **obj.to_dict()})

    def update(self, request, response, **kwargs):
        """
        PUT handler: validate and replace an existing item.
        """
        item_id = int(kwargs.get("id"))
        existing = self.repository.get_by_id(item_id)
        if existing is None:
            response.not_found(f"{self.entity_name} with id {item_id} not found.")
            return

        data = request.json()

        # -- Validate request body --
        errors = self.validator_class.validate_create(data)
        if errors:
            response.bad_request(errors=errors)
            return

        # -- Build updated model and persist --
        obj = self._build_model(data)
        self.repository.update(item_id, obj)
        response.ok(data={"id": item_id, **obj.to_dict()}, message=f"{self.entity_name} updated.")

    def delete(self, request, response, **kwargs):
        """
        DELETE handler: remove an item by ID.
        """
        item_id = int(kwargs.get("id"))
        success = self.repository.delete(item_id)
        if not success:
            response.not_found(f"{self.entity_name} with id {item_id} not found.")
            return
        response.ok(message=f"{self.entity_name} deleted.")

    def _build_model(self, data: dict):
        """
        Build a model instance from validated request data.

        Uses _model_fields to extract values from the data dict
        and pass them as keyword arguments to model_class().

        :param data: validated request body
        :return: new Persistent model instance
        """
        kwargs = {field: data.get(field) for field in self._model_fields}
        return self.model_class(**kwargs)
