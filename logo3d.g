grammar logo3d;

root : proc* stat EOF 
    | proc* EOF
    | stat EOF;

proc : PROC ID '(' arg1 ')' IS stat END;
PROC : 'PROC';
IS : 'IS';
arg1 : ID ',' arg1
    | ID
    |
    ;

stat : assig stat
    | read stat
    | write stat
    | cond stat
    | loop stat
    | invoc stat
    | 
    ;


write : '<<' (expr|boolex);
read : '>>' ID;
assig : ID ':=' (expr|boolex);

invoc : ID '(' arg ')';
arg : (ID | NUM) ',' arg    #ArgSimp
    | (ID | NUM)            #ArgSimp   
    | expr ',' arg          #ArgExpr
    | expr                  #ArgExpr
    |                       #ArgSimp 
    ;

cond : IF boolex THEN stat END
    | IF boolex THEN stat ELSE stat END;
IF : 'IF';
THEN : 'THEN';
ELSE : 'ELSE';
END : 'END'; 

loop : WHILE boolex DO stat END #While
    | FOR ID FROM (NUM | ID) TO (NUM | ID) DO stat END #For
    ;
WHILE : 'WHILE';
DO : 'DO';
FOR : 'FOR';
FROM : 'FROM';
TO : 'TO';

boolex : OP boolex CP
    | boolex ('&&' | '||') boolex
    | boolex ('==' | '!=' | '>' | '<' | '>=' | '<=') boolex
    | ID 
    | NUM
    ;

expr : OP expr CP
    | expr (MULT|DIV) expr
    | expr (SUM|SUB) expr 
    | NUM
    | ID;
idnum : ID | NUM;
CP : ')';
OP : '(';
ID : [a-zA-Z_]+;
NUM : INT | FLOAT;
INT : [0-9]+ ;
FLOAT : INT '.' INT;
SUM : '+' ;
SUB : '-' ;
MULT: '*' ;
DIV : '/' ;
POW : '^' ;

COMMENT: '//' ~[\n]+ -> skip;
WS : [ \n]+ -> skip ;