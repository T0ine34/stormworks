import { App } from '../app.js';

export class NumberDisplay{
    private element : Element;
    private display : Element;
    private _show_decimal : boolean;

    constructor(element : Element){
        this.element = element;
        this._show_decimal = element.getAttribute('data-decimal') === 'true';

        let display = element.querySelector('.display');
        if(!display){
            throw new Error('NumberDisplay element missing .display element');
        }
        this.display = display;

        const channel = this.element.getAttribute('data-channel');
        if(!channel){
            throw new Error('NumberDisplay element missing data-channel attribute');
        }

        new App().registerInputCallback(channel, (value : string) => {
            this.value = parseFloat(value);
        });
    }

    set value(_value : number){
        if(_value){
            if(this._show_decimal){
                this.display.textContent = _value.toFixed(2);
            }
            else{
                this.display.textContent = _value.toFixed(0);
            }
        }
        else{
            this.display.textContent = '0';
        }
    }

    get value() : number{
        return parseFloat(this.display.textContent || '0');
    }
}