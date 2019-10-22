export class Job {
    id: number;
    name: string;
    employer: string;
    url: string;
    date_posted: string;
    seen: boolean;

    public constructor(init?: Partial<Job>) {
        Object.assign(this, init);
    }
}