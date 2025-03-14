export class User{
    id:string | undefined;
    email:string | undefined;
    password:string|undefined;

    constructor(id:string,email:string,password:string){
        this.id = id;
        this.email = email;
        this.password = password;
    }
}