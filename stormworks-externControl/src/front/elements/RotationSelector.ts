import { App } from '../app.js';
import { scale, parseInputMode } from "../utils.js";

enum Direction{
    UP = 'up',
    DOWN = 'down',
    LEFT = 'left',
    RIGHT = 'right'
}

function String2Direction(string : string) : Direction{
    switch(string){
        case 'up':
            return Direction.UP;
        case 'down':
            return Direction.DOWN;
        case 'left':
            return Direction.LEFT;
        case 'right':
            return Direction.RIGHT;
        default:
            throw new Error('Invalid direction string "' + string + '"');
    }
}

function Direction2Angle(direction : Direction) : number{
    switch(direction){
        case Direction.UP:
            return 0;
        case Direction.RIGHT:
            return 90;
        case Direction.DOWN:
            return 180;
        case Direction.LEFT:
            return 270;
        default:
            throw new Error('Invalid direction "' + direction + '"');
    }
}

export class RotationSelector{
    private _angle : number;
    private id : string;
    private _min : number;
    private _max : number;
    private _input : {mode: string, channel: string};
    private _neutral : Direction;
    private _rotator : HTMLElement;
    private _startDragPosition : {x: number, y: number}|null;
    private _startAngle : number|null;
    private _timer : number;


    constructor(element : Element, defaultAngle : number = 0){ // the main div
        this._angle = defaultAngle;
        this.id = element.getAttribute('data-channel') || '';
        this._min = parseFloat(element.getAttribute('data-min') || '0');
        this._max = parseFloat(element.getAttribute('data-max') || '360');
        this._input = parseInputMode(element.getAttribute('data-input') || '');
        this._neutral = String2Direction(element.getAttribute('data-neutral') || 'up');

        if(this._input.mode === 'input'){
            new App().registerInputCallback(this._input.channel, (value : string) => {
                this.angle = scale(parseFloat(value), this._min, this._max, 0, 360) + Direction2Angle(this._neutral);
            });
        }
        else if(this._input.mode === 'output'){
            new App().registerOutputCallback(this._input.channel, (value : string) => {
                this.angle = scale(parseFloat(value), this._min, this._max, 0, 360) + Direction2Angle(this._neutral);
            });
        }

        let rotator = element.querySelector('.rotator'); // the inner div
        if(!rotator){
            throw new Error('RotationSelector element missing .rotator element');
        }
        this._rotator = rotator as HTMLElement;

        let a = scale(defaultAngle, this._min, this._max, 0, 360) + Direction2Angle(this._neutral);
        this._rotator.style.transform = `rotate(${a}deg)`;

        this._startDragPosition = null;
        this._startAngle = null;

        this._timer = Date.now();

        this.registerEventListeners();
    }

    getRelCoords(x : number, y : number) : {x: number, y: number}{
        // return x, y relative to the center of the rotator
        let rect = this._rotator.getBoundingClientRect();
        return {
            x: x - rect.left - rect.width / 2,
            y: y - rect.top - rect.height / 2
        };
    }

    registerEventListeners(){
        this._rotator.addEventListener('mousedown', (event) => {
            this.startRotate(event);
        });
        this._rotator.addEventListener('mouseup', () => {
            this.stopRotate();
        });
        this._rotator.addEventListener('mouseleave', () => {
            this.stopRotate();
        });

        // touch events
        this._rotator.addEventListener('touchstart', (event) => {
            this.startRotate(event);
        });
        this._rotator.addEventListener('touchend', () => {
            this.stopRotate();
        });
    }

    startRotate(event: MouseEvent | TouchEvent){
        if(event.target !== this._rotator){
            return;
        }
        let clientX, clientY : number;
        if (event instanceof MouseEvent) {
            clientX = event.clientX || 0;
            clientY = event.clientY || 0;
        } else {
            clientX = event.touches[0]?.clientX || 0;
            clientY = event.touches[0]?.clientY || 0;
        }
        this._startDragPosition = this.getRelCoords(clientX, clientY);
        this._startAngle = this.angle;
        this._rotator.addEventListener('mousemove', this.rotate);
        this._rotator.addEventListener('touchmove', this.rotate as EventListener);
        this.rotate(event);
    }

    stopRotate(){
        this._rotator.removeEventListener('mousemove', this.rotate);
        this._rotator.removeEventListener('touchmove', this.rotate);
    }

    rotate = (event: MouseEvent | TouchEvent) => {
        let clientX, clientY : number;
        if (event instanceof MouseEvent) {
            clientX = event.clientX || 0;
            clientY = event.clientY || 0;
        } else {
            clientX = event.touches[0]?.clientX || 0;
            clientY = event.touches[0]?.clientY || 0;
        }
        let relCoords = this.getRelCoords(clientX, clientY);
        let angle = Math.atan2(relCoords.y, relCoords.x) * 180 / Math.PI;

        if(this._startDragPosition === null || this._startAngle === null){
            throw new Error('Missing start drag position or start angle');
        }
        
        let delta = angle - Math.atan2(this._startDragPosition.y, this._startDragPosition.x) * 180 / Math.PI;
        this.angle = this._startAngle + delta;
        this.angle = this._startAngle + delta;
        
    }

    set angle(angle : number){
        this._angle = angle;
        this._rotator.style.transform = `rotate(${angle}deg)`;
        
        if(Date.now() - this._timer > 50){ // send value every 50ms
            this.sendValue();
        }
    }

    get angle() : number{
        return this._angle;
    }

    sendValue(){
        this._timer = Date.now();
        let a = this.angle - Direction2Angle(this._neutral);
        if(a < 0){
            a += 360;
        }
        a = scale(a, 0, 360, this._min, this._max);
        let sendValue = a
        new App().update(this.id, sendValue);
    }
}

