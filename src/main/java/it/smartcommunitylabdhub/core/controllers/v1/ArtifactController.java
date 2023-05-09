package it.smartcommunitylabdhub.core.controllers.v1;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import it.smartcommunitylabdhub.core.annotations.ApiVersion;

@RestController
@RequestMapping("/artifacts")
@ApiVersion("v1")
public class ArtifactController {

    @GetMapping("")
    public String artifacts() {
        return "Artifact version 1";
    }

}
