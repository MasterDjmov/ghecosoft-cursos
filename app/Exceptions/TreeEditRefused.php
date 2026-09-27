<?php

namespace App\Exceptions;

use DomainException;

/** El editor del árbol rechaza un cambio (el mensaje se muestra tal cual al docente). */
class TreeEditRefused extends DomainException {}
