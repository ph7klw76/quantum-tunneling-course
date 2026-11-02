export type Edition = 'polished' | 'baseline';
export type LectureProps = {edition: Edition; showCaptions: boolean};
export type Scene = {index:number;title:string;focus:string;kind:string;chapter:number;start_frame:number;end_frame:number;duration_frames:number;speech_end_frame:number};
export type Quiz = {id:string;scene:number;frame:number;question:string;options:string[];correct_index:number;hold_start_frame:number;hold_end_frame:number;answer_reveal_frame:number};
