import { LightningElement } from 'lwc';

export default class ShowInsights extends LightningElement {

    employeeColumns = [
        { label: 'Employee Id', fieldName: 'employeeId' },
        { label: 'First Name', fieldName: 'firstName' },
        { label: 'Last Name', fieldName: 'lastName' },
        { label: 'Phone Number', fieldName: 'employeePhone', type: 'phone' },
        { label: 'Email Address', fieldName: 'employeeEmail', type: 'email' }
    ];

    employeeData = []


    // renderedCallback() { // called whenever component is re-rendered
    connectedCallback() {
        this.getApiData();
    }
    
    getApiData() {
        fetch('https://serverless.abhinav.page/employees/')
        .then(response => {
            console.log(response);
            if(response.ok) {
                return response.json();
            } 
                throw Error(response);
            
        })
        .then(responseData => {
            this.employeeData = responseData
        })
        .catch(error => console.log(error))
        }

}