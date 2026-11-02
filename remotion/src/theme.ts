export const palette={bg:'#081821',panel:'#102B37',ink:'#F1F5EE',muted:'#B8CCD0',teal:'#77E2D3',amber:'#F1BD72',line:'#294753'};
export const font='"Segoe UI", "DejaVu Sans", Arial, sans-serif';
export const phases=['PREDICT','EXPLAIN','COMPUTE','APPLY','CRITIQUE'];
export function phaseFor(index:number,kind:string){return kind==='predict'?0:index>=24?4:index>=20?3:index>=11?2:1;}
