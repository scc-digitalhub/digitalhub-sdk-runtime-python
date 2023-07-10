package it.smartcommunitylabdhub.core.components.runnables.events.messages;

import it.smartcommunitylabdhub.core.components.runnables.events.messages.interfaces.Message;
import it.smartcommunitylabdhub.core.models.dtos.RunDTO;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
public class NuclioMessage implements Message {
    private RunDTO runDTO;
}