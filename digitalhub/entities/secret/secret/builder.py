from __future__ import annotations

from digitalhub.entities._builders.entity import EntityBuilder
from digitalhub.entities.secret.secret.entity import Secret
from digitalhub.entities.secret.secret.spec import SecretSpec, SecretValidator
from digitalhub.entities.secret.secret.status import SecretStatus


class SecretSecretBuilder(EntityBuilder):
    """
    SecretSecret builder.
    """

    ENTITY_CLASS = Secret
    ENTITY_SPEC_CLASS = SecretSpec
    ENTITY_SPEC_VALIDATOR = SecretValidator
    ENTITY_STATUS_CLASS = SecretStatus

    def build(
        self,
        kind: str,
        project: str,
        name: str,
        uuid: str | None = None,
        description: str | None = None,
        labels: list[str] | None = None,
        embedded: bool = True,
        **kwargs,
    ) -> Secret:
        """
        Create a new object.

        Parameters
        ----------
        project : str
            Project name.
        name : str
            Object name.
        kind : str
            Kind the object.
        uuid : str
            ID of the object (UUID4, e.g. 40f25c4b-d26b-4221-b048-9527aff291e2).
        description : str
            Description of the object (human readable).
        labels : list[str]
            List of labels.
        embedded : bool
            Flag to determine if object spec must be embedded in project spec.
        **kwargs : dict
            Spec keyword arguments.

        Returns
        -------
        Secret
            Object instance.
        """
        name = self.build_name(name)
        uuid = self.build_uuid(uuid)
        metadata = self.build_metadata(
            project=project,
            name=name,
            description=description,
            labels=labels,
        )
        path = f"kubernetes://dhcore-proj-secrets-{project}/{name}"
        provider = "kubernetes"
        spec = self.build_spec(
            self.ENTITY_SPEC_CLASS,
            self.ENTITY_SPEC_VALIDATOR,
            path=path,
            provider=provider,
            **kwargs,
        )
        status = self.build_status(self.ENTITY_STATUS_CLASS)
        return self.ENTITY_CLASS(
            project=project,
            name=name,
            uuid=uuid,
            kind=kind,
            metadata=metadata,
            spec=spec,
            status=status,
        )