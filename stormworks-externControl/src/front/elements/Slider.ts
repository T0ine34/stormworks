import { App } from '../app.js';
import { parseInputMode } from "../utils.js";

export class Slider{
    private id : string;
    private slider : HTMLInputElement;
    private decreaseBtn : Element|null;
    private increaseBtn : Element|null;
    private _value : number;

    
    constructor(element : Element, defaultValue : number = 0){ // the main div
        this.id = element.getAttribute('data-channel') || '';

        let slider = element.querySelector('input');
        if(!slider){
            throw new Error('Slider element missing input element');
        }
        this.slider = slider as HTMLInputElement;

        // this._input = parseInputMode(element.getAttribute('data-input'));
        let input = parseInputMode(element.getAttribute('data-input') || '');
        if(!input){
            throw new Error('Slider element missing data-input attribute');
        }
 
        if(input.channel && input.channel === this.id){
            throw new Error('Input channel and element id cannot be the same');
        }
        if(input.mode === 'input'){
            new App().registerInputCallback(input.channel, (value : string) => {
                this.value = parseFloat(value);
                this.slider.value = value;
            });
        }
        else if(input.mode === 'output'){
            new App().registerOutputCallback(input.channel, (value : string) => {
                this.value = parseFloat(value);
                this.slider.value = value;
            });
        }

        this._value = defaultValue;
        this.slider.value = defaultValue.toString();

        this.decreaseBtn = element.querySelector('#decrease-btn');
        this.increaseBtn = element.querySelector('#increase-btn');
        this.registerEventListeners();
    }

    registerEventListeners(){

        this.slider.addEventListener('input', () => {
            this.value = parseFloat(this.slider.value);
        });

        if (this.decreaseBtn === null || this.increaseBtn === null) {
            return;
        }
        this.decreaseBtn.addEventListener('click', () => {
            this.slider.stepDown();
            this.value = parseFloat(this.slider.value);
        });

        this.increaseBtn.addEventListener('click', () => {
            this.slider.stepUp();
            this.value = parseFloat(this.slider.value);
        });
    }

    set value(value : number){
        this._value = value;
        new App().update(this.id, value);
    }

    get value() : number{
        return this._value;
    }
}

