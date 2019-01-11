// https://docs.cypress.io/api/introduction/api.html
/*
describe("My First Test", () => {
  it("Visits the app root url", () => {
    cy.visit("/");
    cy.contains("h1", "Welcome to Your Vue.js App");
  });
});*/
describe("testing the language button", () => {
  it("Visits the app root url", () => {
    cy.visit("/");
  });
  it("Clicks the language button", () => {
    cy.get('[data-cy=cur-locale]')
      .click();
  });
  it("Switches the language", () => {
    cy.get('[data-cy=en-US]')
      .click();
  });
  it("Checks the page to ensure the language changed",() => {
    cy.get('[data-cy=church-sentence]')
      .contains("Church");
      //.contains("Iglesia");
  });
});
