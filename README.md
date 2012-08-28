
[![Documentation][logo]][documentation]
[logo]: src/GAiA/UNIha-user-documentation.textbundle/assets/img/coverpage.png
[documentation]: src/GAiA/UNIha-user-documentation.textbundle/UNIha.pdf

# UNIha

UNIha is short for UNI-C simple high availability for Check Point VPN-1.  It is
a simple active passive hith availability solution which does not require an
aditinal Check Point license. 

### Security

The package installs a separate user, a text based interface and requires
console or ssh access.

## Deployment

The RPM and the installation instruction is found [in RPM](RPM).

The package requires two identical hosts, and the passive hosts monitors
the active for configuration changes using ssh. If detected, a backup of
the active host is initiated and restored on the passive. Next the firewall
software is disabled on the passive and the link between the active and
passive re-established.

## Documentation

[The documentation in pdf is here](src/GAiA/UNIha-user-documentation.textbundle/UNIha.pdf).

For recreating the pdf documentation see
[README-documentation](src/GAiA/UNIha-user-documentation.textbundle/README-documentation.md)
in src/GAiA/UNIha-user-documentation.textbundle.

## Development

The source is written in shell and changes should be easy to adapt.

## License

This is released under a
[modified BSD License](https://opensource.org/licenses/BSD-3-Clause). 

