"""Generate quiz exports, H5P authoring data and a fully executable notebook."""
from pathlib import Path
import csv,json,shutil,sys,textwrap,inspect,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from course.lesson import SEGMENTS,CHAPTERS
import nbformat as nb

QUIZZES=[
 (2,'Must transmission vanish when E < V0?', ['Yes, because every electron is a classical ball.','No; a finite barrier can transmit probability current.','Only if the electron borrows energy.'],1,
  'A finite barrier has a wave solution with nonzero transmitted current. This is a probability prediction, not a classical trajectory.',0),
 (6,'What is continuous at a finite step with constant mass?', ['Only the potential.','Only the wavefunction.','The wavefunction and its first derivative.','The second derivative must always match.'],2,
  'Integrating the Schrödinger equation across a finite step enforces continuity of psi and its first derivative for this constant-mass model.',4),
 (10,'T = 0.1424 predicts what for 10,000 incident electrons?', ['Exactly 1,424 electrons in every trial.','An expected count near 1,424, with fluctuations.','Each electron loses 14.24% of its energy.'],1,
  'Transmission is a probability. For independent electrons the count is binomial, with standard deviation about 35; total energy is conserved.',8),
 (14,'At fixed E = 0.5 eV and V0 = 1 eV, increasing a from 0.45 to 0.90 nm gives:', ['Half the original transmission.','About 0.00587 transmission.','About 0.2847 transmission.'],1,
  'The exact model gives T(0.45) = 0.142362 and T(0.90) = 0.005873. Width dependence is much stronger than a factor of two.',12),
 (18,'Does a static lossless barrier require an energy loan?', ['Yes, for a short enough time.','No; total energy stays conserved.','Yes, if the transmitted wave is small.'],1,
  'The stationary solution has a fixed total energy throughout. Evanescent behavior does not require temporary energy nonconservation.',16),
 (22,'Twice the STM current proves twice the surface height.', ['True.','False; bias, tip and electronic states also matter.','True, because tunneling is linear in distance.'],1,
  'Current is sensitive to gap and electronic structure. Control bias and tip condition and compare spectroscopy; a current ratio is not a height ratio.',20),
 (25,'An exponential thickness trend alone conclusively proves direct tunneling.', ['Yes; no other process can produce that trend.','No; compare controls and competing mechanisms.','No; quantum mechanics forbids any current.'],1,
  'The trend supports tunneling but is not unique. Add temperature and bias series, defect controls, uncertainty and alternative-model comparisons.',24),
]

def main(skip_notebook=False):
    timeline=json.loads((ROOT/'narration/timeline.json').read_text(encoding='utf-8'))
    def ts(t):return f'{int(t)//60:02}:{int(t)%60:02}'
    quizzes=[]
    for i,(seg,q,opts,correct,explain,remedial) in enumerate(QUIZZES):
        quiz_time=float(math.ceil(timeline[seg]['speech_end']+.2))
        quizzes.append(dict(id=f'Q{i+1}',timestamp=ts(quiz_time),
            time_seconds=quiz_time,question=q,options=opts,correct_index=correct,
            explanation=explain,remediation_seconds=round(timeline[remedial]['start'],2),
            incorrect_feedback=['Correct.' if j==correct else 'Reconsider the assumptions. '+explain for j in range(len(opts))]))
    (ROOT/'quizzes/quizzes.json').write_text(json.dumps(quizzes,indent=2),encoding='utf-8')
    with (ROOT/'quizzes/youtube_quizzes.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f);w.writerow(['id','timestamp','question','option_A','option_B','option_C','option_D','answer','explanation'])
        for q in quizzes:w.writerow([q['id'],q['timestamp'],q['question'],*(q['options']+['']*(4-len(q['options']))),chr(65+q['correct_index']),q['explanation']])
    md=['# YouTube quizzes\n\nOne correct answer per item. Insert manually; CSV is an editorial interchange file.\n']
    for q in quizzes:
        md.append(f"## {q['timestamp']} — {q['id']}\n\n{q['question']}\n\n"+'\n'.join(f'{chr(65+j)}. {a}' for j,a in enumerate(q['options']))+f"\n\nAnswer: {chr(65+q['correct_index'])}. {q['explanation']}\n")
    (ROOT/'quizzes/youtube_quizzes.md').write_text('\n'.join(md),encoding='utf-8')
    spec=dict(format='QuantumTunneling.H5P.AuthoringSpecification',version=1,
        notice='Authoring interchange data, not a directly importable .h5p package or H5P content.json.',
        title='Can an Electron Pass Through a Wall?',content_type='Interactive Video',
        media=dict(primary='https://youtu.be/WCA_t3ttAAI',fallback='outputs/Quantum_Tunneling_Lecture.mp4',
                   captions='narration/lecture.srt',duration_seconds=timeline[-1]['start']+timeline[-1]['duration']),
        interactions=[dict(**q,library='H5P.MultiChoice',pause_video=True,display='poster',
            single_answer=True,enable_retry=True,enable_solution=True,
            adaptivity=dict(on_incorrect='Offer a labelled review jump; allow returning to this question.',
                jump_to_seconds=q['remediation_seconds'],require_host_support=True)) for q in quizzes],
        mastery=dict(at_seconds=round(min(timeline[-1]['start']+timeline[-1]['duration']-.05,timeline[-1]['speech_end']+.1),2),
            interaction='Summary task and submit/end screen',pass_guidance='4 of 5 concepts correct, then submit original work; retry permitted.',
            statements=[
                ['A wavefunction predicts measurement statistics, not a particle path.','The curve is the path of one electron.'],
                ['Match psi and its derivative for this finite constant-mass barrier.','Only match probability density.'],
                ['Test T and R using independently solved amplitudes.','Setting R=1-T independently verifies the solver.'],
                ['Exponential thickness dependence alone does not identify a unique mechanism.','Any exponential trend proves tunneling.'],
                ['Report assumptions and uncertainty when interpreting fitted barriers.','A fitted barrier is always a unique material constant.']],correct_statement_index=0),
        host_validation=dict(status='NOT RUN: no Lumi or Moodle authoring host connected.',
            required_checks=['Import the author-created .h5p into a second host.','Play YouTube from student account in actual host.',
                'Verify pause, incorrect feedback, retry, review jumps, summary and submit reporting.','Switch to uploaded MP4 and captions if YouTube is blocked.']))
    (ROOT/'h5p/authoring.json').write_text(json.dumps(spec,indent=2),encoding='utf-8')
    out=ROOT/'website/dist';out.mkdir(parents=True,exist_ok=True)
    shutil.copy(ROOT/'quizzes/quizzes.json',out/'quizzes.json')
    shutil.copy(ROOT/'h5p/authoring.json',out/'h5p-authoring.json')
    chapters=[dict(title=CHAPTERS[i],start=timeline[4*i]['start']) for i in range(7)]
    (out/'chapters.json').write_text(json.dumps(chapters,indent=2),encoding='utf-8')
    description='''# YouTube publication text

Title: Can an Electron Pass Through a Wall? — Quantum Tunneling Explained

Predict, calculate and test quantum tunneling through a finite rectangular barrier. Learn why the wavefunction is not an electron trajectory, solve boundary conditions, and examine STM and electronic interfaces critically.

Companion course: REPLACE_WITH_DEPLOYED_COMPANION_URL
JupyterLite lab: REPLACE_WITH_DEPLOYED_COMPANION_URL/lab/lab/index.html?path=Quantum_Tunneling_Lab.ipynb
H5P version: REPLACE_WITH_YOUR_LUMI_OR_MOODLE_URL
Source and worksheets: REPLACE_WITH_YOUR_SOURCE_REPOSITORY_URL

CHAPTERS
'''+ '\n'.join(ts(c['start'])+' '+c['title'] for c in chapters)+'''

Default model: free electron, E = 0.50 eV, V0 = 1.00 eV, a = 0.45 nm; T = 0.142362. Static 1D elastic barrier with identical leads. Real interfaces may require effective masses, band structure, fields, defects and inelastic processes.

Pause at each prediction prompt before continuing. External H5P and JupyterLite activities open on the companion platform; they do not run inside YouTube's native player.

Original course text and visuals: CC BY 4.0. Code: MIT. NARRATION_CREDIT. No music or third-party photos.

References: https://openstax.org/books/university-physics-volume-3/pages/7-6-the-quantum-tunneling-of-particles-through-potential-barriers
https://www.nobelprize.org/prizes/physics/1986/summary/

#QuantumTunneling #QuantumMechanics #Physics #MaterialsScience
'''
    neural=ROOT/'outputs/neural-narration-report.json'
    if neural.exists() and timeline[0].get('engine') in ('chatterbox','kokoro'):
        voice=json.loads(neural.read_text(encoding='utf-8'))
        credit='Locally generated AI narration: '+('Chatterbox TTS (MIT model/code), with synthetic conditioning from the official Kokoro-82M af_heart stock voice (Apache 2.0)' if voice['engine']=='chatterbox' else 'Kokoro-82M, official af_heart voicepack (Apache 2.0)')
    else:credit='Legacy offline synthetic narration: eSpeak NG, GPL-3.0-or-later engine'
    description=description.replace('NARRATION_CREDIT',credit)
    (ROOT/'outputs/youtube_description.md').write_text(description,encoding='utf-8')
    if not skip_notebook:notebook()
    print(f'Authored {len(quizzes)} quizzes, H5P specification, chapters and upload text; notebook '+('preserved.' if skip_notebook else 'generated.'))

def notebook():
    cells=[]
    md=lambda t:cells.append(nb.v4.new_markdown_cell(inspect.cleandoc(t)))
    code=lambda t:cells.append(nb.v4.new_code_cell(inspect.cleandoc(t)))
    md('''# Quantum Tunneling Laboratory
    **Predict → calculate → test → explain → revise.** Browser Python (Pyodide); no widget extension is required.

    Work in order. Change `E`, `V0`, and `a` in the parameter cell and rerun subsequent cells. Download your completed notebook: browser storage is local to this browser and origin. First launch needs internet to download Pyodide and packages.

    Learning goals: explain transmission as current, derive boundary conditions, compare independent calculations, evaluate evidence, and report model limitations.
    ''')
    md('''## 1. Predict before running
    For E = 0.50 eV, V0 = 1.00 eV and a = 0.45 nm, predict whether T is zero, small, or near one. Predict the effect of doubling width. Record a reason and confidence (0–100%).

    **Your prediction:** …
    ''')
    code('''import sys
    if sys.platform == "emscripten":
        import piplite
        await piplite.install(["numpy", "scipy", "matplotlib"])
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.integrate import solve_ivp
    from scipy.stats import linregress
    print("Python ready:", sys.platform)
    ''')
    # Standalone definitions avoid browser-filesystem import assumptions.
    source=(ROOT/'course/physics.py').read_text(encoding='utf-8')
    code(source)
    code('''# Edit these inputs, then Run All Below. Energies eV, length nm.
    E = 0.50
    V0 = 1.00
    a = 0.45
    validate(E, V0, a)
    T = transmission(E,V0,a)
    r,A,B,t = amplitudes(E,V0,a)
    R = abs(r)**2
    print(f"T={T:.9f}, R={R:.9f}, T+R={T+R:.12f}")
    print(f"kappa={np.sqrt((V0-E)/C):.6f} nm^-1")
    assert abs(T+R-1)<1e-10
    ''')
    md('''## 2. Read the state carefully
    Left: incident plus reflected waves. Right: outgoing only. The plotted real part is one phase choice. The stationary density is |psi|². A unit incident amplitude is a flux convention, not normalization over all space. Explain why ripples on the left do not imply electrons move up and down along the curve.
    ''')
    code('''x = np.linspace(-1, a+1, 1200)
    psi, derivative = wavefunction(x,E,V0,a)
    potential = np.where((x>=0)&(x<=a), V0, 0)
    fig,axes=plt.subplots(2,1,figsize=(10,6),sharex=True)
    axes[0].plot(x,potential,color="black",label="V (eV)")
    axes[0].axhline(E,color="crimson",ls="--",label="E (eV)")
    axes[0].set_ylabel("Energy (eV)");axes[0].legend()
    axes[1].plot(x,psi.real,label="Re(psi), relative amplitude")
    axes[1].plot(x,abs(psi)**2,label="|psi|², relative density")
    axes[1].axvspan(0,a,color="gray",alpha=.15)
    axes[1].set(xlabel="x (nm)",ylabel="Relative scale");axes[1].legend()
    plt.tight_layout();plt.show()
    # Current divided by incident current, proportional to Im(psi* dpsi/dx).
    current = np.imag(psi.conj()*derivative)/np.sqrt(E/C)
    assert np.max(abs(current-T))<1e-9
    print("Constant normalized current:", current.min(), current.max())
    ''')
    code('''widths=np.linspace(0,1.2,200)
    energies=np.linspace(.01,V0*.99,200)
    fig,axes=plt.subplots(1,2,figsize=(10,4))
    axes[0].semilogy(widths,[transmission(E,V0,w) for w in widths])
    axes[0].set(xlabel="Width (nm)",ylabel="T",title="Fixed energy and height")
    axes[1].plot(energies,[transmission(e,V0,a) for e in energies])
    axes[1].set(xlabel="Energy (eV)",ylabel="T",title="Fixed width and height")
    plt.tight_layout();plt.show()
    print("Exact T(2a)/T(a):",transmission(E,V0,2*a)/T)
    ''')
    md('''## 3. Independent numerical calculation
    Integrate the Schrödinger ODE backwards with psi(a)=1 and psi′(a)=ik. Resolve the incident amplitude at x=0 and compute its inverse squared magnitude. This does not reuse the closed-form transmission expression.

    Predict what happens when the integration tolerance is loosened. For very opaque barriers this integration can suffer cancellation; investigate a moderate range first.
    ''')
    code('''for tolerance in [1e-4,1e-7,1e-10]:
        numerical=numerical_transmission(E,V0,a,rtol=tolerance)
        print(f"rtol={tolerance:g}: T_num={numerical:.10f}, error={abs(numerical-T):.3g}")
    np.testing.assert_allclose(numerical,T,rtol=1e-7)
    # A second check: boundary matching gives independently evaluated R and T.
    np.testing.assert_allclose(abs(t)**2+abs(r)**2,1,atol=1e-10)
    ''')
    md('''## 4. Find and repair a model error
    The following intentionally incorrect function mixes electron volts and nanometers with SI constants. Execute it, explain the dimensional error, then implement a repaired version without calling `transmission` inside it. Compare your repaired result with the reference.
    ''')
    code('''def wrong_model(E_eV,V_eV,a_nm):
        wrong_kappa=np.sqrt(2*M_E*(V_eV-E_eV))/HBAR
        # Illustrates the wrong exponent without overflowing sinh.
        return np.exp(-2*wrong_kappa*a_nm)
    print("Intentionally wrong output:",wrong_model(E,V0,a))
    # TODO: define repaired_model(E_eV,V_eV,a_nm) and test its dimensions.
    ''')
    md('''## 5. Design and critique an experiment
    **Synthetic data below are generated, not measured device evidence.** Fit log(current) versus thickness. Decide what the slope can and cannot establish. Add a second candidate mechanism: an activated current `I0 * exp(-Ea/(k_B*T_temperature))`. Predict a temperature sweep for each mechanism and identify confounds.
    ''')
    code('''rng=np.random.default_rng(7)
    measured_width=np.linspace(.25,.9,12)
    # 10% log-normal instrumental/scatter illustration; uncertainty model is assumed.
    current_data=np.array([transmission(.5,1,w) for w in measured_width])*np.exp(rng.normal(0,.10,12))
    fit=linregress(measured_width,np.log(current_data))
    print(f"log-slope={fit.slope:.3f} +/- {fit.stderr:.3f} nm^-1 (one standard error)")
    plt.errorbar(measured_width,current_data,yerr=.1*current_data,fmt="o",label="synthetic data")
    plt.plot(measured_width,np.exp(fit.intercept+fit.slope*measured_width),label="log-linear fit")
    plt.yscale("log");plt.xlabel("Thickness (nm)");plt.ylabel("Relative current");plt.legend();plt.show()
    # TODO: plot activated and weakly temperature-dependent candidate predictions.
    ''')
    md('''## 6. Independent transfer task and submission
    A new interface has an estimated effective mass `0.20*m_e` and a triangular rather than rectangular barrier under bias. You may not simply reuse the free-electron rectangular formula unchanged.

    1. Derive how kappa changes if a constant effective mass were appropriate, and state the new interface matching assumptions.
    2. Design a numerical solution for the triangular barrier and outline a convergence test.
    3. Propose thickness, temperature, and bias measurements to compare direct tunneling, activation, and defect transport. Include instrument leakage and morphology controls.
    4. Explain parameter uncertainty and identifiability: can one current measurement uniquely determine height and width?
    5. Submit original code, a plot, a dimensional check, a boundary/current check, and a 300-word evidence argument. Revisit your initial prediction and confidence.

    **Reflection / evidence argument:** …

    Assessment rubric and pre/post/delayed tasks are in `docs/assessment.md`. Code MIT; original lesson text CC BY 4.0. Constants: CODATA 2022 free-electron mass, SI electron volt and reduced Planck constant as stated in the code.
    ''')
    book=nb.v4.new_notebook(cells=cells,metadata={'kernelspec':{'display_name':'Python (Pyodide)','language':'python','name':'python'},'language_info':{'name':'python','version':'3.12'}})
    nb.validate(book)
    target=ROOT/'lab/files';target.mkdir(parents=True,exist_ok=True)
    nb.write(book,target/'Quantum_Tunneling_Lab.ipynb')
    shutil.copy(target/'Quantum_Tunneling_Lab.ipynb',ROOT/'lab/Quantum_Tunneling_Lab.ipynb')
    shutil.copy(target/'Quantum_Tunneling_Lab.ipynb',ROOT/'website/dist/Quantum_Tunneling_Lab.ipynb')

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--skip-notebook',action='store_true')
    main(parser.parse_args().skip_notebook)
