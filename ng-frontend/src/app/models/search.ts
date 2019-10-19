export class Search {
    pattern: string;
   
    public constructor(init?: Partial<Search>) {
        Object.assign(this, init);
    }
}