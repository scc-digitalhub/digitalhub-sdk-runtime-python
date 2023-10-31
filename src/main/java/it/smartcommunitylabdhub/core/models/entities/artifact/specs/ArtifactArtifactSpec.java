package it.smartcommunitylabdhub.core.models.entities.artifact.specs;

import it.smartcommunitylabdhub.core.annotations.common.SpecType;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.specs.SpecEntity;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@SpecType(kind = "artifact", entity = SpecEntity.ARTIFACT)
public class ArtifactArtifactSpec extends ArtifactBaseSpec {
}