import { App } from '../app.js';
import { clamp } from "../utils.js";

export class Keypad{
    private id : string;
    private _min : number;
    private _max : number;
    private _value : string;
    private _display : Element;
    private _buttons : NodeListOf<Element>;
    private _timeout : NodeJS.Timeout|null;

    constructor(element : Element, defaultValue : string = ""){ // the main div
        // this.id = element.getAttribute('data-channel');
        // this._min = element.getAttribute('data-min');
        // this._max = element.getAttribute('data-max');
        let id = element.getAttribute('data-channel');
        if(!id){
            throw new Error('Keypad element missing data-channel attribute');
        }
        this.id = id;

        let min = element.getAttribute('data-min');
        if(min){
            this._min = parseFloat(min);
        }
        else{
            this._min = -Infinity;
        }

        let max = element.getAttribute('data-max');
        if(max){
            this._max = parseFloat(max);
        }
        else{
            this._max = Infinity;
        }
        
        this._value = defaultValue;
        if (!this._isValueValid(this._value)) {
            this._value = '0';
        }

        let display = element.querySelector('.keypad-display');
        if(!display){
            throw new Error('Keypad element missing .keypad-display element');
        }
        this._display = display;

        let buttons = element.querySelectorAll('.keypad-button');
        if(!buttons){
            throw new Error('Keypad element missing .keypad-button elements');
        }
        this._buttons = buttons;

        this._timeout = null;

        this.registerEventListeners();
    }

    _isValueValid(value : string) : boolean {
        if (isNaN(parseFloat(value))) {
            return false;
        }

        if (parseFloat(value) < this._min || parseFloat(value) > this._max) {
            return false;
        }

        return true;
    }

    registerEventListeners(){
        this._buttons.forEach((button) => {
            button.addEventListener('click', () => {
                let value = button.getAttribute('data-value');
                if (value === 'backspace') {
                    this.value = this.value.toString().slice(0, -1);
                }
                else if (value === 'minus') {
                    this.value = (-this.value).toString();
                }
                else if (value === 'circle') {
                    if (!this.value.toString().includes('.')) {
                        this.value = this.value.toString() + '.';
                    }
                }
                else {
                    this.value += value;
                }
            });
        });
    }

    set value(value : string){
        if (!this._isValueValid(value)) {
            return;
        }
        this._value = value;
        this._display.textContent = this._value;
        if (this._timeout) {
            clearTimeout(this._timeout);
        }
        this._timeout = setTimeout(() => {
            this.sendValue();
        }, 1000); // 1 second
    }    
    
    get value() : string{
        return this._value;
    }

    sendValue(){
        let sendValue = parseFloat(this._value);
        if (this._value === "") {
            sendValue = clamp(0, this._min, this._max);
        }
        this._display.textContent = sendValue.toString();
        new App().update(this.id, sendValue);
    }
}