import { App } from '../app.js';
import { parseBool, parseInputMode } from "../utils.js";

export class PushButton{
    private _state : boolean;
    private element : Element;
    private id : string;

    constructor(element : Element){
        this._state = false;
        this.element = element;
        // this.id = element.getAttribute('data-channel');
        let id = element.getAttribute('data-channel');
        if(!id){
            throw new Error('PushButton element missing data-channel attribute');
        }
        this.id = id;

        let input = parseInputMode(element.getAttribute('data-input') || '');
        if(input.mode === 'input'){
            new App().registerInputCallback(input.channel, (value : string) => {
                this.state = parseBool(value);
            });
        }
        else if(input.mode === 'output'){
            new App().registerOutputCallback(input.channel, (value : string) => {
                this.state = parseBool(value);
            });
        }

        this.element.addEventListener('mousedown', () => {
            this.state = true;
        });
        this.element.addEventListener('mouseup', () => {
            this.state = false;
        });

        // touch events
        this.element.addEventListener('touchstart', () => {
            this.state = true;
        });
        this.element.addEventListener('touchend', () => {
            this.state = false;
        });
    }

    set state(value : boolean){
        this._state = value;
        new App().update(this.id, value);
        if(this.state){
            this.element.classList.add('active');
        }else{
            this.element.classList.remove('active');
        }
    }

    get state() : boolean{
        return this._state;
    }
}