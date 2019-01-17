describe("Create Team Test", function() {
  before(() => {
    cy.login();
  });

  it("GIVEN: Event planner goes to teams page", function() {
    cy.visit("/teams/all");
  });

  it("WHEN: Event planner creates a new team", function() {
    cy.get("[data-cy=add-team]").click();

    cy.get("[data-cy=description]").type("A cool new worship team.");

    cy.get("[data-cy=form-save]").click();
  });

  it("THEN: A new team is listed", function() {
    cy.get("tbody").contains("A cool new worship team.");
  });
});