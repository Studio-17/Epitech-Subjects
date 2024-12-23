# 42sh

> Timeline: 3 semaines

> Nombre de personnes sur le projet: 4

<br>

📂---[B-PSU-200_42sh.pdf](https://github.com/Studio-17/Epitech-Subjects/blob/main/Semester-2/B-PSU-200/42sh/B-PSU-200_42sh.pdf)


<br>


<details>
<summary> Tests de la moulinette </summary>
<table align="center">
    <thead>
        <tr>
            <td colspan="3" align="center"><strong>MOULINETTE</strong></td>
        </tr>
        <tr>
            <th>SOMMAIRE</th>
            <th>NB DE TESTS</th>
            <th>DETAILS</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan="4">01 - basic tests</td>
            <td rowspan="4" style="text-align: center;">4</td>
            <td>Empty</td>
        </tr>
    		<tr>
			<td>Simple exec</td>
		</tr>
		<tr>
			<td>run simple commands</td>
		</tr>
		<tr>
			<td>wrong simple command</td>
		</tr>
        <tr>
            <td rowspan="5">02 - path handling</td>
            <td rowspan="5" style="text-align: center;">5</td>
            <td>PATH 1</td>
        </tr>
    		<tr>
			<td>PATH 2</td>
		</tr>
		<tr>
			<td>PATH 3</td>
		</tr>
		<tr>
			<td>PATH 4</td>
		</tr>
		<tr>
			<td>PATH 5</td>
		</tr>
        <tr>
            <td rowspan="2">03 - setenv and unsetenv</td>
            <td rowspan="2" style="text-align: center;">2</td>
            <td>setenv and unsetenv</td>
        </tr>
    		<tr>
			<td>setenv and unsetenv with special values</td>
		</tr>
        <tr>
            <td rowspan="3">04 - builtin cd</td>
            <td rowspan="3" style="text-align: center;">3</td>
            <td>cd</td>
        </tr>
    		<tr>
			<td>cd and error messages</td>
		</tr>
		<tr>
			<td>cd-</td>
		</tr>
        <tr>
            <td rowspan="8">05 - line formatting (space and tabs)</td>
            <td rowspan="8" style="text-align: center;">8</td>
            <td>space 1</td>
        </tr>
    		<tr>
			<td>space 2</td>
		</tr>
		<tr>
			<td>space 3</td>
		</tr>
		<tr>
			<td>space 4</td>
		</tr>
		<tr>
			<td>space and tab</td>
		</tr>
		<tr>
			<td>tab 1</td>
		</tr>
		<tr>
			<td>tab 2</td>
		</tr>
		<tr>
			<td>tab 3</td>
		</tr>
        <tr>
            <td rowspan="6">06 - error handling</td>
            <td rowspan="6" style="text-align: center;">6</td>
            <td>Bin not compatible</td>
        </tr>
    		<tr>
			<td>DivZero with core dump</td>
		</tr>
		<tr>
			<td>DivZero without core dump</td>
		</tr>
		<tr>
			<td>SegFault with core dump</td>
		</tr>
		<tr>
			<td>SegFault without core dump</td>
		</tr>
		<tr>
			<td>exec a directory</td>
		</tr>
        <tr>
            <td rowspan="1">07 - separator</td>
            <td rowspan="1" style="text-align: center;">1</td>
            <td>separator ;</td>
        </tr>
        <tr>
            <td rowspan="3">08 - simple pipe</td>
            <td rowspan="3" style="text-align: center;">3</td>
            <td>Pipe with builtin</td>
        </tr>
    		<tr>
			<td>pipe</td>
		</tr>
		<tr>
			<td>pipe with big input</td>
		</tr>
        <tr>
            <td rowspan="6">09 - advanced pipe</td>
            <td rowspan="6" style="text-align: center;">6</td>
            <td>Multipipe and Error</td>
        </tr>
    		<tr>
			<td>error and pipe</td>
		</tr>
		<tr>
			<td>multipipe</td>
		</tr>
		<tr>
			<td>multipipe and FDMAX</td>
		</tr>
		<tr>
			<td>only a pipe</td>
		</tr>
		<tr>
			<td>pipe and error</td>
		</tr>
        <tr>
            <td rowspan="5">10 - redirections</td>
            <td rowspan="5" style="text-align: center;">5</td>
            <td>big file input redirect</td>
        </tr>
    		<tr>
			<td>input redirect</td>
		</tr>
		<tr>
			<td>output double-redirect</td>
		</tr>
		<tr>
			<td>output redirect</td>
		</tr>
		<tr>
			<td>redirect on bin and big files</td>
		</tr>
        <tr>
            <td rowspan="3">11 - advanced manipulations</td>
            <td rowspan="3" style="text-align: center;">3</td>
            <td>Long command line with multiple redirect and pipe</td>
        </tr>
    		<tr>
			<td>redirect output on input</td>
		</tr>
		<tr>
			<td>running mysh inside mysh</td>
		</tr>
        <tr>
            <td rowspan="3">12 - && and || tests</td>
            <td rowspan="3" style="text-align: center;">3</td>
            <td>&&</td>
        </tr>
    		<tr>
			<td>&& and ||</td>
		</tr>
		<tr>
			<td>||</td>
		</tr>
        <tr>
            <td rowspan="1">13 - globbing</td>
            <td rowspan="1" style="text-align: center;">1</td>
            <td>globbing</td>
        </tr>
        <tr>
            <td rowspan="3">14 - var interpreter</td>
            <td rowspan="3" style="text-align: center;">3</td>
            <td>advanced</td>
        </tr>
    		<tr>
			<td>environment</td>
		</tr>
		<tr>
			<td>local</td>
		</tr>
        <tr>
            <td rowspan="2">15 - inhibitor</td>
            <td rowspan="2" style="text-align: center;">2</td>
            <td>advanced inhibitor</td>
        </tr>
    		<tr>
			<td>inhibitor</td>
		</tr>
        <tr>
            <td rowspan="3">16 - magic quote</td>
            <td rowspan="3" style="text-align: center;">3</td>
            <td>exec result of magic quote</td>
        </tr>
    		<tr>
			<td>pipe with magic quote</td>
		</tr>
		<tr>
			<td>simple</td>
		</tr>
        <tr>
            <td rowspan="4">17 - alias</td>
            <td rowspan="4" style="text-align: center;">4</td>
            <td>alias loop</td>
        </tr>
    		<tr>
			<td>alias of alias</td>
		</tr>
		<tr>
			<td>alias with args</td>
		</tr>
		<tr>
			<td>simple</td>
		</tr>
        <tr>
            <td rowspan="1">18 - scripting</td>
            <td rowspan="1" style="text-align: center;">1</td>
            <td>just simple command</td>
        </tr>
        <tr>
            <td rowspan="1">19 - foreach</td>
            <td rowspan="1" style="text-align: center;">1</td>
            <td>foreach</td>
        </tr>
        <tr>
            <td rowspan="2">20 - which</td>
            <td rowspan="2" style="text-align: center;">2</td>
            <td>which</td>
        </tr>
    		<tr>
			<td>which error</td>
		</tr>
        <tr>
            <td rowspan="2">21 - where</td>
            <td rowspan="2" style="text-align: center;">2</td>
            <td>where</td>
        </tr>
    		<tr>
			<td>where error</td>
		</tr>
        <tr>
            <td rowspan="2">22 - if</td>
            <td rowspan="2" style="text-align: center;">2</td>
            <td>if</td>
        </tr>
    		<tr>
			<td>if and foreach</td>
		</tr>
        <tr>
            <td rowspan="1">23 - repeat</td>
            <td rowspan="1" style="text-align: center;">1</td>
            <td>repeat</td>
        </tr>
        <tr>
            <td rowspan="1">24 - parenthesis</td>
            <td rowspan="1" style="text-align: center;">1</td>
            <td>repeat</td>
        </tr>
    
	</tbody>
</table>
</details>

<br>

[↩️ Revenir au module](https://github.com/Studio-17/Epitech-Subjects/blob/main/Semester-2/B-PSU-200)

[↩️ Revenir au Semester-2](https://github.com/Studio-17/Epitech-Subjects/blob/main/Semester-2)

[↩️ Revenir à l'accueil](https://github.com/Studio-17/Epitech-Subjects)

<br>

---

<div align="center">

<a href="https://github.com/Studio-17" target="_blank"><img src="../../../assets/voc17.gif" width="40"></a>

</div>