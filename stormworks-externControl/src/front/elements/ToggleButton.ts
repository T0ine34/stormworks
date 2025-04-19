import { App } from '../app.js';
import { parseBool, parseInputMode } from "../utils.js";

export class ToggleButton{
    private _state : boolean;
    private element : Element;
    private id : string;

    constructor(element : Element, defaultValue = false){
        this._state = parseBool(defaultValue);
        this.element = element;
        this.id = element.getAttribute('data-channel') || '';
        this.element.addEventListener('click', () => {
            this.state = !this.state;
        });

        // this._input = parseInputMode(element.getAttribute('data-input'));
        let input = parseInputMode(element.getAttribute('data-input') || '');
        if(!input){
            throw new Error('ToggleButton element missing data-input attribute');
        }
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
