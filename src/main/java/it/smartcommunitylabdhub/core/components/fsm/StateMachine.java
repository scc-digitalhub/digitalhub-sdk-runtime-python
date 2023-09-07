/**
 * StateMachine.java
 *
 * This class represents a State Machine that handles the flow of states and transitions based on
 * events and guards. It allows the definition of states and transitions along with their associated
 * actions and guards.
 *
 * @param <S> The type of the states.
 * @param <E> The type of the events.
 * @param <C> The type of the context.
 */

package it.smartcommunitylabdhub.core.components.fsm;

import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.UUID;
import java.util.function.BiConsumer;
import java.util.function.Consumer;
import lombok.Getter;
import lombok.Setter;
import lombok.extern.log4j.Log4j2;

@Getter
@Setter
@Log4j2
public class StateMachine<S, E, C> {
    private String uuid;
    private S currentState;
    private S errorState;
    private Map<S, State<S, E, C>> states;
    private Map<E, Consumer<C>> eventListeners;
    private BiConsumer<S, C> stateChangeListener;
    private HashMap<S, Consumer<Optional<C>>> entryActions;
    private HashMap<S, Consumer<Optional<C>>> exitActions;
    private Context<C> initialContext;

    /**
     * Default constructor to create an empty StateMachine.
     */
    public StateMachine() {}

    /**
     * Constructor to create a StateMachine with the initial state and context.
     *
     * @param initialState The initial state of the StateMachine.
     * @param initialContext The initial context for the StateMachine.
     */
    public StateMachine(S initialState, Context<C> initialContext) {
        this.uuid = UUID.randomUUID().toString();
        this.currentState = initialState;
        this.errorState = null;
        this.states = new HashMap<>();
        this.eventListeners = new HashMap<>();
        this.entryActions = new HashMap<>();
        this.exitActions = new HashMap<>();
        this.initialContext = initialContext;
    }

    /**
     * Static builder method to create a new StateMachine.
     *
     * @param initialState The initial state of the StateMachine.
     * @param initialContext The initial context for the StateMachine.
     * @return A new Builder instance to configure and build the StateMachine.
     */
    public static <S, E, C> Builder<S, E, C> builder(S initialState, Optional<C> initialContext) {
        return new Builder<>(initialState, initialContext);
    }

    // Builder
    public static class Builder<S, E, C> {
        private S currentState;
        private S errorState;
        private Map<S, State<S, E, C>> states;
        private Map<E, Consumer<C>> eventListeners;
        private BiConsumer<S, C> stateChangeListener;
        private HashMap<S, Consumer<Optional<C>>> entryActions;
        private HashMap<S, Consumer<Optional<C>>> exitActions;
        private Context<C> initialContext;

        public Builder(S initialState, Optional<C> initialContext) {
            this.currentState = initialState;
            this.initialContext = new Context<C>(initialContext);
            this.states = new HashMap<>();
            this.eventListeners = new HashMap<>();
            this.entryActions = new HashMap<>();
            this.exitActions = new HashMap<>();
        }

        public Builder<S, E, C> withState(S state, State<S, E, C> stateDefinition) {
            states.put(state, stateDefinition);
            return this;
        }

        public Builder<S, E, C> withErrorState(S errorState, State<S, E, C> stateDefinition) {
            this.errorState = errorState;

            // Add the error state to the states map if it doesn't exist
            states.putIfAbsent(errorState, stateDefinition);
            return this;
        }

        public <T> Builder<S, E, C> withEventListener(E eventName, Consumer<C> listener) {
            eventListeners.put(eventName, listener);
            return this;
        }

        public Builder<S, E, C> withStateChangeListener(BiConsumer<S, C> listener) {
            stateChangeListener = listener;
            return this;
        }


        /**
         * Set the entry action for a specific state.
         *
         * @param state The state for which to set the entry action.
         * @param entryAction The entry action as a Consumer instance.
         */
        public Builder<S, E, C> withEntryAction(S state, Consumer<Optional<C>> entryAction) {
            entryActions.put(state, entryAction);
            return this;
        }

        /**
         * Set the exit action for a specific state.
         *
         * @param state The state for which to set the exit action.
         * @param exitAction The exit action as a Consumer instance.
         */
        public Builder<S, E, C> withExitAction(S state, Consumer<Optional<C>> exitAction) {
            exitActions.put(state, exitAction);
            return this;
        }

        public StateMachine<S, E, C> build() {
            StateMachine<S, E, C> stateMachine = new StateMachine<>(currentState, initialContext);
            stateMachine.states = states;
            stateMachine.errorState = errorState;
            stateMachine.eventListeners = eventListeners;
            stateMachine.stateChangeListener = stateChangeListener;
            stateMachine.entryActions = entryActions;
            stateMachine.exitActions = exitActions;
            return stateMachine;
        }

    }

    /**
     * Transition the state machine to the specified target state following a valid path.
     *
     * This method attempts to transition the state machine to the target state by following a valid
     * path of states. It performs the following steps: 1. Checks if a valid path exists from the
     * current state to the target state. 2. Copies the state machine's context to the first state
     * in the path. 3. Follows the path and for each state: a. Applies the internal logic of the
     * target state. b. Executes the exit action of the current state. c. Executes the entry action
     * of the next state. 4. Finally, copies the context to the target state.
     *
     * @param targetState The state to transition to.
     * @param <T> The type of the result from applying the logic.
     * @return An optional result from applying the logic of the target state, or empty if the path
     *         is invalid.
     */
    @SuppressWarnings("unchecked")
    public <T> Optional<T> goToState(S targetState) {

        // Check if a valid path exists from the current state to the target state
        List<S> path = findPath(currentState, targetState);
        if (path.isEmpty()) {
            // No valid path exists; transition to the error state
            return goToErrorState();
        }

        // Copy State Machine context to first state
        try {
            states.get(currentState).setContext((Context<C>) initialContext.clone());
        } catch (CloneNotSupportedException e) {
            e.printStackTrace();
        }

        // Follow the path
        // 1. apply internal logic
        // 2. execute exit action
        // 3. execute entry action of the current state.
        for (int i = 0; i < path.size() - 1; i++) {

            // Get state definition
            S stateInPath = path.get(i);
            State<S, E, C> stateDefinition = states.get(stateInPath);

            // Apply internal logic of the target state
            stateDefinition.getInternalLogic()
                    .map(internalFunc -> applyInternalFunc(
                            (contextStateValue, stateMachineValue) -> internalFunc.applyLogic(
                                    contextStateValue,
                                    stateMachineValue),
                            currentState)) // Optional.empty() because no input is provided
                    .orElse(Optional.empty());



            // execute exit action
            Consumer<Optional<C>> exitAction = exitActions.get(stateInPath);
            if (exitAction != null) {
                exitAction.accept(stateDefinition.getContext().getValue());
            }

            // Get next state if exist and execute logic

            Optional.ofNullable(path.get(i + 1)).ifPresent(nextState -> {

                // Copy state machine context to next state if present otherwise set to null
                try {
                    states.get(nextState)
                            .setContext((Context<C>) states.get(currentState).getContext().clone());
                } catch (CloneNotSupportedException e) {
                    e.printStackTrace();
                }


                // Retrieve the transition event dynamically
                Optional<E> transitionEvent = stateDefinition.getTransitionEvent(nextState);

                if (transitionEvent.isPresent()) {
                    // Notify event listeners for the transition event
                    notifyEventListeners(currentState, transitionEvent.get());
                }


                // Update the current state and notify state change listener
                currentState = nextState;

                // Notify listener for state changed
                notifyStateChangeListener(currentState);

                // Execute entry action
                Optional.ofNullable(entryActions.get(nextState))
                        .ifPresent(action -> action
                                .accept(stateDefinition.getContext().getValue()));

            });
        }
        return null;
    }



    @SuppressWarnings("unchecked")
    // Implement the goToErrorState method to transition to the error state
    private <T> Optional<T> goToErrorState() {
        if (errorState != null) {
            try {
                states.get(errorState)
                        .setContext((Context<C>) states.get(currentState).getContext().clone());
            } catch (CloneNotSupportedException e) {
                e.printStackTrace();
            }
            currentState = errorState;
            State<S, E, C> errorStateDefinition = states.get(errorState);
            if (errorStateDefinition != null) {
                // Execute error logic
                return (Optional<T>) errorStateDefinition.getInternalLogic()
                        .map(internalFunc -> applyInternalFunc(
                                (contextStateValue, stateMachineValue) -> internalFunc.applyLogic(
                                        contextStateValue,
                                        stateMachineValue),
                                currentState)) // Optional.empty() because no input is provided
                        .orElse(Optional.empty());
            } else {
                throw new IllegalStateException(
                        "Invalid error state: " + errorState + " : " + this.getUuid());
            }
        } else {
            throw new IllegalStateException("Error state not set" + " : " + this.getUuid());
        }
    }

    /**
     * Find a path from the source state to the target state in the state machine.
     *
     * This method initiates a depth-first search (DFS) to explore the state machine's transitions
     * and find a valid path from the source state to the target state.
     *
     * @param sourceState The starting state of the path.
     * @param targetState The state to reach.
     * @return A list of states representing a valid path from the source state to the target state,
     *         or an empty list if no valid path is found.
     */
    private List<S> findPath(S sourceState, S targetState) {
        Set<S> visited = new HashSet<>();
        LinkedList<S> path = new LinkedList<>();

        // Call the recursive DFS function to find the path
        if (dfs(sourceState, targetState, visited, path)) {
            // If a valid path exists, return it
            return path;
        } else {
            // If no valid path exists, return an empty list
            return Collections.emptyList();
        }
    }

    /**
     * Depth-First Search (DFS) function to find a path between two states in the state machine.
     *
     * This function explores the state machine's transitions in a depth-first manner to find a path
     * from the current state to the target state.
     *
     * @param currentState The current state being explored.
     * @param targetState The target state to reach.
     * @param visited A set to keep track of visited states during the search.
     * @param path A linked list to record the current path being explored.
     * @return True if a valid path is found from the current state to the target state, otherwise
     *         false.
     */
    private boolean dfs(S currentState, S targetState, Set<S> visited, LinkedList<S> path) {
        // Mark the current state as visited and add it to the path
        visited.add(currentState);
        path.addLast(currentState);

        // If the current state is the target state, a valid path is found
        if (currentState.equals(targetState)) {
            return true;
        }

        // Get the current state's definition
        State<S, E, C> stateDefinition = states.get(currentState);

        // Iterate over the transitions from the current state
        for (E event : stateDefinition.getTransactions().keySet()) {
            Transaction<S, E, C> transaction = stateDefinition.getTransactions().get(event);

            // Check if the next state in the transaction is unvisited
            if (!visited.contains(transaction.getNextState())) {

                // Recursively search for a path from the next state to the target state
                if (dfs(transaction.getNextState(), targetState, visited, path)) {
                    return true; // A valid path is found
                }
            }
        }

        // If no valid path is found from the current state, backtrack
        path.removeLast();
        return false;
    }



    /**
     * Applies the internal logic associated with a state, allowing for customized handling of state
     * transitions and updates to the state machine's context.
     *
     * @param stateLogic The state logic implementation to apply.
     * @param state The current state for which the internal logic is executed.
     * @param <T> The type of result returned by the state logic.
     * @return An optional result obtained from applying the internal logic, or empty if not
     *         applicable.
     */
    private <T> Optional<T> applyInternalFunc(StateLogic<S, E, C, T> stateLogic, S state) {
        Optional<C> context = states.get(state).getContext().getValue();
        return stateLogic.applyLogic(context.orElse(null), this);
    }


    /**
     * Notifies the state change listener, if registered, about a state transition.
     *
     * @param newState The new state to which the state machine has transitioned.
     */
    private void notifyStateChangeListener(S newState) {
        if (stateChangeListener != null) {
            stateChangeListener.accept(newState, initialContext.getValue().orElse(null));
        }
    }

    /**
     * Notifies event listeners, if registered, about an event associated with a state.
     *
     * @param state The current state from which the event is triggered.
     * @param eventName The event name that occurred.
     */
    private <T> void notifyEventListeners(S state, E eventName) {
        Optional<C> context = states.get(state).getContext().getValue();
        Consumer<C> listener = (Consumer<C>) eventListeners.get(eventName);
        if (listener != null) {
            listener.accept(context.orElse(null));

        }
    }
}
