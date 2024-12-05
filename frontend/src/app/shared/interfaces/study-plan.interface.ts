import { Domain } from "./domain.interface";
import { Topic } from "./topic.interface";
import { User } from "./user.interface";

export interface StudyPlan {
    topics?: Topic[];
    id?: number;
    title: string;
    visibility: Domain;
    author?: User;
    deleted?: boolean;
}