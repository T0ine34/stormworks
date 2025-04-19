import { App } from '../app.js';
import {strip} from "../utils.js";

export class RGBDisplay{
    private element : Element;
    private _r : number;
    private _g : number;
    private _b : number;

    constructor(element : Element){
        this.element = element;
        let channels = strip(element.getAttribute('data-channel') || '').split(',');
        if(channels.length !== 3){
            throw new Error('RGBDisplay element missing data-channel attribute');
        }

        this._r = 0;
        this._g = 0;
        this._b = 0;
        new App().registerInputCallback(strip(channels[0]), (value : string) => {
            this.r = parseFloat(value);
        });
        new App().registerInputCallback(strip(channels[1]), (value : string) => {
            this.g = parseFloat(value);
        });
        new App().registerInputCallback(strip(channels[2]), (value : string) => {
            this.b = parseFloat(value);
        });
    }

    update(){
        let color = `rgb(${this.r}, ${this.g}, ${this.b})`;
        let icon = this.element.querySelector('.icon') as HTMLElement;
        if(!icon){
            throw new Error('RGBDisplay element missing .icon element');
        }
        // if icon has 'svg' class
        if(icon.classList.contains('svg')){
            icon.style.fill = color;
            icon.style.stroke = color;
        }
        else{
            icon.style.color = color;
        }
    }

    set r(value : number){
        this._r = value;
        this.update();
    }

    get r() : number{
        return this._r;
    }

    set g(value : number){
        this._g = value;
        this.update();
    }

    get g() : number{
        return this._g;
    }

    set b(value : number){
        this._b = value;
        this.update();
    }

    get b() : number{
        return this._b;
    }
}