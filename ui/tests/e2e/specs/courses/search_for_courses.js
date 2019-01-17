describe("Get to Courses Page", () => {
    it("Given Successfull login", () => {
      cy.login()
    });
  
    it("When: clicking to course page", () => {
      cy.get("[data-cy=open-navigation]").click();
      cy.get('[data-cy=courses-admin]').click();
    });
    it("Then: should be in course page", () => {
      cy.url().should("include", "/courses");
    });
});

describe("search for courses that exist", () => {
    it("When: course name is typed", () => {
        cy.get('[data-cy=courses-table-search]').type('COS')
    });
    it("Then: should find course name", () => {
        cy.get('tbody > :nth-child(1) > :nth-child(1)').contains("COS");
    });
});

describe("search for courses that does not exist", () => {
    it("When: course name is typed", () => {
        cy.get('[data-cy=courses-table-search]').clear().type('Help')
    });
    it("Then: should find nothing", () => {
        cy.get('tbody > :nth-child(1) > :nth-child(1)').contains("No se encontraron registros coincidentes");
    });
});

