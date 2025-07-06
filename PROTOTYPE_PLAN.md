# Prototype Plan for US Inheritance Calculator

This document outlines a lightweight approach to build an inheritance calculator prototype covering multiple US states. The goal is to support the key differences in intestacy laws (the default distribution when someone dies without a will) for a small set of states.

## Target States

The initial prototype will include the following six states:

1. **Texas (TX)** – already implemented.
2. **New York (NY)** – already implemented.
3. **California (CA)**
4. **Florida (FL)**
5. **Michigan (MI)**
6. **Illinois (IL)**

## High-Level Design

1. **Common Core**
   - Use a base calculator class that handles generic per-stirpes distribution of descendants.
   - Represent people and relationships in a simple tree structure (already provided in `core.tree`).
   - Use Pydantic models in `core.models` to validate inputs and unify fields (estate size, spouse flag, children, etc.).

2. **State Modules**
   - For each state, subclass the base calculator and override the `spouse_share` method to apply that state’s intestacy rules regarding surviving spouses.
   - Optionally override `descendants_share` if a state deviates from standard per-stirpes.
   - Register each state in `states.__init__.py` so the API can look up the proper calculator.

3. **API Layer**
   - FastAPI (already in `app.py` and `api.routes`) exposes a `/calculate` endpoint that accepts the `EstateInput` payload and returns the distribution.

## User Input Flow

The minimal front-end should present a form that mirrors the key data in `EstateInput`:

1. **Select State** – dropdown for `TX`, `NY`, `CA`, `FL`, `MI`, `IL`.
2. **Enter Date of Death** – enables future historical logic.
3. **Valid Will?** – if `Yes`, the API simply returns the estate to the beneficiaries listed in the will.
4. **Family Information** – checkboxes / counts:
   - Surviving spouse?
   - Number of children (each child can be marked as stepchild, adopted, or predeceased with descendants).
   - Parents alive? / Siblings alive?
5. **Asset Information (optional)** – total estate value and any community-property portion (used by TX and CA).

Submitting this form sends a POST request to `/calculate` with a JSON body that matches `EstateInput`. The response is a mapping of heirs to shares, which the front-end can display along with an explanation of the applied state rules.

## Example State Rules (Simplified)

Below is a high-level summary of intestacy rules that the prototype can model. These are simplified for demonstration and should not be used as legal advice.

### Texas
- Community property: spouse keeps their half; if all children are with the spouse, the spouse inherits the decedent’s community half. For separate property, the spouse typically receives one-third if there are descendants.

### New York
- Spouse receives $50k plus half of the remainder if descendants exist; otherwise the spouse takes everything.

### California (to implement)
- Community property: spouse already owns one-half and inherits the other half if all children are shared. Separate property is divided with spouse taking one-third when there are two or more children.

### Florida (to implement)
- Spouse inherits everything if all descendants are also descendants of the spouse. Otherwise, spouse receives one-half and descendants share the other half.

### Michigan (to implement)
- Spouse receives the first $150k plus a percentage of the remainder depending on whether there are children or parents surviving (often one-half when there are descendants).

### Illinois (to implement)
- If a spouse and descendants survive, the spouse receives one-half of the estate and the descendants share the remaining half per stirpes.

## Implementation Steps

1. **Add Enum Values** – `State` enum already lists the six states.
2. **Create Calculator Classes** – For CA, FL, MI, and IL, create modules in `states/` similar to `texas.py` and `new_york.py` implementing each state’s spouse rules.
3. **Update Registry** – Update `states/__init__.py` to register each new calculator.
4. **Expand Tests** – Create example payloads in `tests/` for each state to ensure calculations run without errors.
5. **Run FastAPI** – Launch the API with `uvicorn app:app` and send POST requests to `/calculate` with JSON payloads representing the estate and family tree.

## Data Sources

The above summaries are derived from publicly available information on each state’s probate or intestacy statutes. For production use, consult up-to-date legal references or an attorney to ensure accuracy.

