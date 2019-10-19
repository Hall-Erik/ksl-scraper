export class User {
    pk: number;
    username: string;
    email: string;
   
    public constructor(init?: Partial<User>) {
        Object.assign(this, init);
    }
}