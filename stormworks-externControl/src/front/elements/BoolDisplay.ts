import { App } from '../app.js';
import {parseBool} from "../utils.js";

export class BoolDisplay{
    private element : Element;

    constructor(element : Element){
        this.element = element;
        const channel = this.element.getAttribute('data-channel');
        if(!channel){
            throw new Error('BoolDisplay element missing data-channel attribute');
        }
        new App().registerInputCallback(channel, (value : string) => {
            this.state = parseBool(value);
        });
    }

    set state(value : boolean){
        if(value){
            this.element.classList.add('active');
        }
        else{
            this.element.classList.remove('active');
        }
    }

    get state() : boolean{
        return this.element.classList.contains('active');
    }
}